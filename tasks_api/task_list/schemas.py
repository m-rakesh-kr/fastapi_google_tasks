from datetime import datetime
from pydantic import BaseModel
from tasks_api.users.schemas import UserRegisterResponse


class BaseTaskList(BaseModel):
    list_name: str
    user_id: int


class TaskList(BaseModel):
    list_name: str

    class Config:
        orm_mode = True


class ShowTaskList(BaseModel):
    id: str
    list_name: str
    user_id: int

    # creator = UserRegisterResponse

    class Config:
        orm_mode = True


class ShowStarredTask(BaseModel):
    title: str
    details: str
    date_time: datetime

    # creator = UserRegisterResponse
    class Config:
        orm_mode = True
