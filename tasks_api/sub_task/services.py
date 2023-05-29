from sqlalchemy.orm import Session
from . import schemas, models
from tasks_api.users.models import User
from tasks_api.task_list.models import TaskList
from tasks_api.task.models import Task
from fastapi import HTTPException, status
from tasks_api import constants


def create_sub_task(task_id: int, request: schemas.ShowSubTask, db: Session, current_user):
    user = User.get_user_by_email(db, current_user.email)
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=constants.MSG_TASK_NOT_FOUND.format(task_id))
    if task.list.creator != user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=constants.MSG_TASK_NOT_FOUND.format(task_id))

    new_sub_task = models.SubTask(title=request.title, details=request.details, date_time=request.date_time,
                                  task_id=task_id)
    db.add(new_sub_task)
    db.commit()
    db.refresh(new_sub_task)
    return new_sub_task


def show_all_sub_task(task_id: int, db: Session, date, current_user):
    user = User.get_user_by_email(db, current_user.email)
    task = (
        db.query(Task)
        .join(TaskList)
        .filter(Task.id == task_id, TaskList.user_id == user.id, Task.list_id == TaskList.id)
        .first()
    )
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=constants.MSG_TASK_NOT_FOUND2.format(task_id))

    sub_task_query = (
        db.query(models.SubTask)
        .join(Task)
        .filter(Task.id == task_id, models.SubTask.task_id == task_id)
    )
    # if date:
    #     sub_task_query = sub_task_query.order_by(models.SubTask.date_time.desc())
    # else:
    #     sub_task_query = sub_task_query.order_by(models.SubTask.title.asc())

    sub_task_query = sub_task_query.order_by(models.SubTask.date_time.asc() if date else models.SubTask.title.desc())

    sub_task_all = sub_task_query.all()
    return sub_task_all


def show_one_sub_task(sub_task_id: int, db: Session, current_user):
    user = User.get_user_by_email(db, current_user.email)
    sub_task = (
        db.query(models.SubTask)
        .join(Task)
        .join(TaskList)
        .filter(models.SubTask.id == sub_task_id, Task.list_id == TaskList.id, TaskList.user_id == user.id)
        .first()
    )
    if not sub_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=constants.MSG_SUB_TASK_NOT_FOUND.format(sub_task_id))
    return sub_task


def update_sub_task(sub_task_id: int, request: schemas.ShowSubTask, starred, db: Session, current_user):
    user = User.get_user_by_email(db, current_user.email)
    sub_task = (
        db.query(models.SubTask)
        .join(Task)
        .join(TaskList)
        .filter(models.SubTask.id == sub_task_id, Task.list_id == TaskList.id, TaskList.user_id == user.id)
        .first()
    )
    if not sub_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=constants.MSG_SUB_TASK_NOT_FOUND.format(sub_task_id))

    # if sub_task.task.list.creator.email != current_user.email:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                         detail=constants.MSG_SUB_TASK_UPDATE_FORBIDDEN)

    sub_task.title = request.title
    sub_task.details = request.details
    sub_task.date_time = request.date_time
    sub_task.starred = starred
    db.commit()

    return {"message": constants.MSG_SUB_TASK_UPDATED}


def delete_sub_task(sub_task_id: int, db: Session, current_user):
    user = User.get_user_by_email(db, current_user.email)
    sub_task = (
        db.query(models.SubTask)
        .join(Task)
        .join(TaskList)
        .filter(models.SubTask.id == sub_task_id, Task.list_id == TaskList.id, TaskList.user_id == user.id)
        .first()
    )
    if not sub_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=constants.MSG_SUB_TASK_NOT_FOUND.format(sub_task_id))

    # if sub_task.task.list.creator != current_user:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                         detail=constants.MSG_SUB_TASK_DELETE_FORBIDDEN)

    db.delete(sub_task)
    db.commit()

    return {"message": constants.MSG_SUB_TASK_DELETED}
