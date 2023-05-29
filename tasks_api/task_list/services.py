from sqlalchemy.orm import Session
from . import schemas, models
from fastapi import HTTPException, status
from tasks_api import constants
from tasks_api.users.models import User
from tasks_api.task_list.models import TaskList
from tasks_api.task.models import Task
from tasks_api.sub_task.models import SubTask


def show_starred_task(db: Session, current_user):
    user = User.get_user_by_email(db, current_user.email)
    task_list = db.query(TaskList).filter(TaskList.user_id == user.id).all()
    # Here creating query's objects of all the task_list
    starred_task = []
    # here creating blank list that will contain all the starred tasks of tasks and sub_tasks
    for tl in task_list.copy():
        # .copy -> creating “real copies” or “clones” of these objects, which will not affect the original obj.
        task = db.query(Task).filter(Task.starred == True, Task.list_id == tl.id).all()
        # Here, will create query's obj of all the starred tasks whose id belong to task_list.id
        starred_task.extend(task)
        # Here extending all objects of starred task which belong to user's task_list

    # Now, I have to find all the starred sub_tasks of current user.
    for t in task_list:
        task_obj = db.query(Task).filter(Task.list_id == t.id).all()
        # It will create obj of all the tasks whose list_id will belong to current user.
        for to in task_obj.copy():
            # .copy -> creating “real copies” or “clones” of these objects, which will not affect the original obj.
            sub_task = db.query(SubTask).filter(SubTask.starred == True, SubTask.task_id == to.id).all()
            # here finding all the starred sub_tasks of individual tasks.
            starred_task.extend(sub_task)
        # here adding starred sub_tasks into tasks
    return starred_task


def create_task_list(request: schemas.TaskList, db: Session, current_user):
    # current_user = authorize.get_jwt_subject()
    user = User.get_user_by_email(db, current_user.email)
    new_task_list = models.TaskList(list_name=request.list_name, user_id=user.id)
    db.add(new_task_list)
    db.commit()
    db.refresh(new_task_list)
    return new_task_list


def show_all_task_list(db: Session, current_user):
    user = User.get_user_by_email(db, current_user.email)
    task_list = db.query(models.TaskList).filter(models.TaskList.user_id == user.id).all()
    return task_list


def show_one_task_list(list_id: int, db: Session, current_user):
    user = User.get_user_by_email(db, current_user.email)
    task_list = db.query(models.TaskList).filter(models.TaskList.user_id == user.id,
                                                 models.TaskList.id == list_id).first()
    if not task_list:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=constants.MSG_TASK_LIST_NOT_FOUND.format(list_id))
    return task_list


def update_task_list(list_id: int, request: schemas.TaskList, db: Session, current_user):
    user = User.get_user_by_email(db, current_user.email)
    tasklist = db.query(models.TaskList).filter(models.TaskList.id == list_id,
                                                models.TaskList.user_id == user.id)

    if not tasklist.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=constants.MSG_TASK_LIST_NOT_FOUND.format(list_id))

    tasklist.update({"list_name": request.list_name}, synchronize_session='evaluate')
    db.commit()
    update_status = {
        "message": constants.MSG_TASK_LIST_UPDATED
    }
    return update_status


def delete_task_list(list_id: int, db: Session, current_user):
    user = User.get_user_by_email(db, current_user.email)
    tasklist = db.query(models.TaskList).filter(models.TaskList.id == list_id,
                                                models.TaskList.user_id == user.id)
    if not tasklist.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=constants.MSG_TASK_LIST_NOT_FOUND.format(list_id))

    tasklist.delete(synchronize_session='evaluate')
    db.commit()
    delete_status = {
        "message": constants.MSG_TASK_LIST_DELETED
    }
    return delete_status
