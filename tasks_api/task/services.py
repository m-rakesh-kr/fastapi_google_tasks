from sqlalchemy.orm import Session, joinedload
from . import schemas, models
from tasks_api.task_list.models import TaskList
from tasks_api.users.models import User
from fastapi import HTTPException, status
from tasks_api import constants


def create_task(list_id: int, request: schemas.ShowTask, db: Session, current_user):
    # user = db.query(User).filter(User.email == current_user.email).first()
    user = User.get_user_by_email(db, current_user.email)
    task_list = db.query(TaskList).options(joinedload(TaskList.task)).filter(TaskList.id == list_id,
                                                                             TaskList.user_id == user.id).first()
    if not task_list:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=constants.MSG_TASK_LIST_NOT_FOUND2.format(list_id))

    new_task = models.Task(title=request.title, details=request.details, date_time=request.date_time,
                           list_id=list_id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


def show_all_task(list_id: int, db: Session, current_user, date):
    user = User.get_user_by_email(db, current_user.email)
    task_list = db.query(TaskList).options(joinedload(TaskList.tasks)).filter(TaskList.id == list_id,
                                                                              TaskList.user_id ==user.id ).first()
    if not task_list:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=constants.MSG_TASK_LIST_NOT_FOUND2.format(list_id))

    tasks = task_list.tasks
    if not tasks:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=constants.MSG_TASK_LIST_NOT_FOUND2.format(list_id))

    if date:
        return sorted(tasks, key=lambda task: task.date_time)
    return sorted(tasks, key=lambda task: task.title)


def show_one_task(task_id: int, db: Session, current_user):
    user = User.get_user_by_email(db, current_user.email)
    task = db.query(models.Task).join(TaskList).filter(models.Task.id == task_id,
                                                       TaskList.user_id == user.id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=constants.MSG_TASK_NOT_FOUND.format(task_id))

    return task


def update_task(task_id: int, request: schemas.ShowTask, starred, db: Session, current_user):
    user = User.get_user_by_email(db, current_user.email)
    task = db.query(models.Task).join(TaskList).filter(models.Task.id == task_id,
                                                       TaskList.user_id == user.id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=constants.MSG_TASK_NOT_FOUND.format(task_id))

    task.title = request.title
    task.details = request.details
    task.date_time = request.date_time
    task.starred = starred

    db.commit()

    return {"message": constants.MSG_TASK_UPDATED}


def delete_task(task_id: int, db: Session, current_user):
    user = User.get_user_by_email(db, current_user.email)
    task = db.query(models.Task).join(TaskList).filter(models.Task.id == task_id,
                                                       TaskList.user_id == user.id).first()

    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=constants.MSG_TASK_NOT_FOUND.format(task_id))

    db.delete(task)
    db.commit()

    return {"message": constants.MSG_TASK_DELETED}
