from typing import List
from fastapi import APIRouter, Depends, status
from tasks_api.users import oauth2, schemas as user_schemas
from . import schemas
from database import get_db
from sqlalchemy.orm import Session
from . import services

# Creating routing for Tasks...............
router = APIRouter(
    prefix="/api/v1",
    tags=['Task']
)


@router.post('/create/{list_id}/task', status_code=status.HTTP_201_CREATED)
def create(list_id: int, request: schemas.Task, db: Session = Depends(get_db),
           current_user: user_schemas.UserModel = Depends(
               oauth2.get_current_user)):
    """
    This is call when request method is Post.
    :param list_id:
    :param current_user:
    :param request:
    :param db:
    :return: status msg
    """
    return services.create_task(list_id, request, db, current_user)


@router.get('/get_all/{list_id}/task', response_model=List[schemas.ShowTask], status_code=status.HTTP_200_OK)
def show_all(list_id: int, db: Session = Depends(get_db), date: str | None = None,
             current_user: user_schemas.UserModel = Depends(oauth2.get_current_user)):
    """
    This is call when request method is Get.
    :param date: Query param for sort by date. if you want to sorted by date result then pass date = something.
    :param list_id:
    :param current_user:
    :param db:
    :return: list of Task
    """
    return services.show_all_task(list_id, db, current_user, date)


@router.get('/get_one/{task_id}/task', response_model=schemas.ShowTask, status_code=status.HTTP_200_OK)
def show(task_id: int, db: Session = Depends(get_db),
         current_user: user_schemas.UserModel = Depends(oauth2.get_current_user)):
    """
    This is call when request method is Get.
    :param task_id:
    :param current_user:
    :param db:
    :return: Task
    """
    return services.show_one_task(task_id, db, current_user)


@router.put('/update/{task_id}/task', status_code=status.HTTP_200_OK)
def update(task_id: int, request: schemas.Task, starred: bool = False, db: Session = Depends(get_db),
           current_user: user_schemas.UserModel = Depends(oauth2.get_current_user)):
    """
    This is call when request method is Updated.
    :param task_id:
    :param starred: If you want to star your task then pass ?starred=True.
    :param current_user:
    :param request:
    :param db:
    :return: Update status
    """
    print()
    return services.update_task(task_id, request, starred, db, current_user)


@router.delete('/delete/{list_id}/task', status_code=status.HTTP_200_OK)
def delete(list_id: int, db: Session = Depends(get_db),
           current_user: user_schemas.UserModel = Depends(oauth2.get_current_user)):
    """
    This is call when request method is deleted.
    :param current_user:
    :param list_id:
    :param db:
    :return: delete status
    """
    return services.delete_task(list_id, db, current_user)


