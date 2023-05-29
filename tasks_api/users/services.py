from sqlalchemy.orm import Session
from . import schemas, models
from fastapi import HTTPException, status
from .hashing import Hasher
from tasks_api import constants
from . import tokens
from .schema_validations import check_confirm_password
from .tasks import send_user_creation_mail, send_reset_password_mail


def create_user(request, db):
    exist_user = db.query(models.User).filter(models.User.email == request.email).first()
    if exist_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=constants.ERR_EMAIL_ALREADY_TAKEN.format(request.email))
    else:
        check_confirm_password(request.password, request.confirm_password)
        new_user = models.User(name=request.name, email=request.email, password=Hasher.bcrypt(request.password))
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        send_user_creation_mail.delay([new_user.email], new_user.name)
        return new_user


def user_login(request, db):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=constants.MSG_INVALID_CREDENTIALS)
    if not Hasher.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=constants.MSG_INVALID_PASSWORD)

    access_token = tokens.create_token(constants.JWT_SECRET_KEY, constants.ALGORITHM,
                                       constants.ACCESS_TOKEN_EXPIRE_MINUTES, data={"sub": user.email})
    refresh_tokens = tokens.create_token(constants.JWT_REFRESH_SECRET_KEY, constants.ALGORITHM,
                                         constants.REFRESH_TOKEN_EXPIRE_MINUTES, data={"sub": user.email})
    return {"access_token": access_token, "refresh-token": refresh_tokens, "token_type": "bearer"}


def show_user(user_id: int, db: Session):
    user = db.query(models.User).get(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=constants.MSG_USER_NOT_AVAILABLE.format(user_id))
    return user


def refresh_token(email):
    return tokens.create_token(constants.JWT_REFRESH_SECRET_KEY, constants.ALGORITHM,
                               constants.REFRESH_TOKEN_EXPIRE_MINUTES, data={"sub": email})


def forgot_password(request, db: Session):
    user = db.query(models.User).filter(models.User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=constants.EMAIL_NOT_EXIST.format(request.email))
    forgot_password_token = tokens.create_token(constants.JWT_FORGOT_PASSWORD_SECRET_KEY, constants.ALGORITHM,
                                                constants.FORGOT_PASSWORD_EXPIRE_MINUTES, data={"sub": user.email})
    reset_password_link = constants.RESET_PASSWORD_LINK + '/' + forgot_password_token
    send_reset_password_mail.delay([user.email], user.name, reset_password_link)
    return {"Reset Password Link": reset_password_link}


def reset_password(reset_token, request, db: Session):
    email = tokens.verify_token(constants.JWT_FORGOT_PASSWORD_SECRET_KEY, constants.ALGORITHM, reset_token,
                                HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                              detail=constants.INVALID_EXPIRED_TOKEN_MSG))
    if not email:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=constants.USER_NOT_FOUND_OF_TOKEN_MSG)

    check_confirm_password(request.password, request.confirm_password)

    email = getattr(email, 'email')

    user_data = db.query(models.User).filter(models.User.email == email).first()
    user_data.password = Hasher.bcrypt(request.password)

    db.commit()
    return {"message": "Password Reset Successfully"}
