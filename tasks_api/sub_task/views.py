from __future__ import annotations

from typing import List
from fastapi import APIRouter, Depends, status
from tasks_api.users import oauth2, schemas as user_schemas
from . import schemas
from database import get_db
from sqlalchemy.orm import Session
from . import services

# Creating routing for Sub Tasks...............
router = APIRouter(
    prefix="/api/v1",
    tags=['Sub Task']
)


@router.post('/create/{task_id}/sub_task', status_code=status.HTTP_201_CREATED)
def create(task_id: int, request: schemas.SubTask, db: Session = Depends(get_db),
           current_user: user_schemas.UserModel = Depends(
               oauth2.get_current_user)):
    """
    This is call when request method is Post.
    :param task_id:
    :param current_user:
    :param request:
    :param db:
    :return: create status
    """
    return services.create_sub_task(task_id, request, db, current_user)


@router.get('/get_all/{task_id}/sub_task', response_model=List[schemas.ShowSubTask], status_code=status.HTTP_200_OK)
def show_all(task_id: int, db: Session = Depends(get_db), date_by: str | None = None,
             current_user: user_schemas.UserModel = Depends(oauth2.get_current_user)):
    """
    This is call when request method is Get.
    :param date_by: Query param for sort by date. if you want to sorted by date result then pass date = something.
    :param task_id:
    :param current_user:
    :param db:
    :return: list of Sub Task
    """
    return services.show_all_sub_task(task_id, db, date_by, current_user)


@router.get('/get_one/{sub_task_id}/sub_task', response_model=schemas.ShowSubTask, status_code=status.HTTP_200_OK)
def show(sub_task_id: int, db: Session = Depends(get_db),
         current_user: user_schemas.UserModel = Depends(oauth2.get_current_user)):
    """
    This is call when request method is Get.
    :param sub_task_id:
    :param current_user:
    :param db:
    :return: Sub Task
    """
    return services.show_one_sub_task(sub_task_id, db, current_user)


@router.put('/update/{sub_task_id}/sub_task', status_code=status.HTTP_200_OK)
def update(sub_task_id: int, request: schemas.SubTask, starred: bool = False, db: Session = Depends(get_db),
           current_user: user_schemas.UserModel = Depends(oauth2.get_current_user)):
    """
    This is call when request method is Updated.
    :param starred: If you want to star your task then pass ?starred=True.
    :param current_user:
    :param request:
    :param sub_task_id:
    :param db:
    :return: update status
    """
    return services.update_sub_task(sub_task_id, request, starred, db, current_user)


@router.delete('/delete/{sub_task_id}/sub_task', status_code=status.HTTP_200_OK)
def delete(sub_task_id: int, db: Session = Depends(get_db),
           current_user: user_schemas.UserModel = Depends(oauth2.get_current_user)):
    """
    This is call when request method is deleted.
    :param current_user:
    :param sub_task_id:
    :param db:
    :return: delete status
    """
    return services.delete_sub_task(sub_task_id, db, current_user)
