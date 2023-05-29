from typing import List
from fastapi import APIRouter, Depends, status

from tasks_api.users import oauth2, schemas as user_schemas
from . import schemas
from database import get_db
from sqlalchemy.orm import Session
from . import services

router = APIRouter(
    prefix="/api/v1",
    tags=['Task List and Starred Task']
)


@router.post('/show_all/starred_task', response_model=List[schemas.ShowStarredTask], status_code=status.HTTP_200_OK)
def show_all(db: Session = Depends(get_db),
             current_user: user_schemas.UserModel = Depends(oauth2.get_current_user)):
    """
    This is call when request method is Post
    :param current_user:
    :param db:
    :return: status msg
    """
    return services.show_starred_task(db, current_user)


@router.post('/create/task_list', status_code=status.HTTP_201_CREATED, )
def create(request: schemas.TaskList, db: Session = Depends(get_db),
           current_user: user_schemas.UserModel = Depends(
               oauth2.get_current_user)):
    """
    This is call when request method is Post.
    :param current_user:
    :param request:
    :param db:
    :return: status msg
      """
    return services.create_task_list(request, db, current_user)


@router.get('/get_all/task_list/', response_model=List[schemas.ShowTaskList], status_code=status.HTTP_200_OK)
def show_all(db: Session = Depends(get_db),
             current_user: user_schemas.UserModel = Depends(oauth2.get_current_user)):
    """
    This is call when request method is Get.
    :param current_user:
    :param db:
    :return: list of TaskList
    """
    return services.show_all_task_list(db, current_user)


@router.get('/get_one/{list_id}/task_list', response_model=schemas.ShowTaskList, status_code=status.HTTP_200_OK)
def show(list_id: int, db: Session = Depends(get_db),
         current_user: user_schemas.UserModel = Depends(oauth2.get_current_user)):
    """
    This is call when request method is Get.
    :param current_user:
    :param list_id:
    :param db:
    :return: TaskList
    """
    return services.show_one_task_list(list_id, db, current_user)


@router.put('/update/{list_id}/task_list', status_code=status.HTTP_200_OK)
def update(list_id: int, request: schemas.TaskList, db: Session = Depends(get_db),
           current_user: user_schemas.UserModel = Depends(
               oauth2.get_current_user)):
    """
    This is call when request method is Updated.
    :param current_user:
    :param request:
    :param list_id:
    :param db:
    :return: Update msg
    """
    return services.update_task_list(list_id, request, db, current_user)


@router.delete('/delete/{list_id}/task_list', status_code=status.HTTP_200_OK)
def delete(list_id: int, db: Session = Depends(get_db),
           current_user: user_schemas.UserModel = Depends(oauth2.get_current_user)):
    """
    This is call when request method is deleted.
    :param current_user:
    :param list_id:
    :param db:
    :return: status msg
    """
    return services.delete_task_list(list_id, db, current_user)
