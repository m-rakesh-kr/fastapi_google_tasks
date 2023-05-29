from fastapi_mail import FastMail, MessageSchema
from fastapi.responses import JSONResponse
from tasks_api.utils import MailConfig
from . import schemas, oauth2
from database import get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status
from . import services
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import BackgroundTasks
from .tasks import send_user_creation_mail

router = APIRouter(
    tags=['Users']
)


@router.get("/api/v1/auth/test_server", status_code=status.HTTP_200_OK)
async def server_check():
    """
    A Simple function to check if server is working state or not
    :return: str: Simple message
    """
    return "Server is working"


@router.post('/api/v1/auth/register', response_model=schemas.UserRegisterResponse, status_code=status.HTTP_201_CREATED)
async def create(request: schemas.UserRegisterRequest, db: Session = Depends(get_db)):
    """
    This is call when request method is post.
    :param db:
    :param request: schema request data
    :return: Created username and email
    """
    return services.create_user(request, db)


@router.post('/api/v1/auth/login')
async def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    This is call when request method is post
    :param request: schema request login data
    :param db:
    :return: JWT Bearer access and refresh tokens
    """
    return services.user_login(request, db)


@router.get('/api/v1/auth/user/{user_id}', response_model=schemas.ShowUser)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    This is call when request method is Get
    :param db:
    :param user_id:
    :return: user's email
    """
    return services.show_user(user_id, db)


@router.get('/api/v1/auth/refresh_token')
async def refresh_token(current_user: schemas.UserModel = Depends(oauth2.get_current_user)):
    """
    This is call when request method is Get
    :param current_user:
    :return: JWT refresh-token
    """
    token = services.refresh_token(current_user.email)
    return {"refresh_token": token}


@router.post('/api/v1/auth/forgot_password')
async def forgot_password(request: schemas.ForgotPassword, db: Session = Depends(get_db)):
    """
    This is call when request method is Get.
    :param request:
    :param db:
    :return: Reset Password token
    """
    return services.forgot_password(request, db)


@router.post('/api/v1/auth/reset_password/{reset_token}')
async def reset_password(reset_token: str, request: schemas.ResetPassword, db: Session = Depends(get_db)):
    """
    This is call when request method is Get.
    :param reset_token:
    :param request:
    :param db:
    :return: Status msg
    """
    return services.reset_password(reset_token, request, db)


# @router.post('/send-email')
# async def send_email(background_tasks: BackgroundTasks, email: schemas.EmailSchema):
#     """
#       THis is testing of send mail using BackgroundTasks module and This is call when request method is POST.
#       :email: valid email
#       :return: Email has been sent successfully message!
#     """
#     content = {'title': 'Task Alert', 'name': 'Rakesh Kumar'}
#     msg_schema = MessageSchema(
#         subject="Fastapi mail module",
#         recipients=email.dict().get("email"),
#         template_body=content
#     )
#     fm = FastMail(MailConfig.connection_config())
#     # await fm.send_message(msg_schema, template_name="alert_msg.html")
#     background_tasks.add_task(fm.send_message, msg_schema, template_name="email.html")
#     return JSONResponse(status_code=200, content={"message": "Email has been sent! check you email"})
#

# @router.post('/send_mail_using_celery')
# async def send_mail_celery(email: schemas.UserEmail):
#     send_user_creation_mail.delay([email.email])  # Pass the email address as a string
#     return "User creation mail sent successfully!"
