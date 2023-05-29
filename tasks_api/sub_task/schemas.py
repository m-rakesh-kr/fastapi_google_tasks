from pydantic import BaseModel
from datetime import datetime


class BaseSubTask(BaseModel):
    title: str
    details: str
    date_time: datetime


class SubTask(BaseModel):
    title: str
    details: str
    date_time: datetime

    class Config:
        orm_mode = True


class ShowSubTask(BaseModel):
    id: str
    title: str
    details: str
    date_time: datetime
    task_id: str

    class Config:
        orm_mode = True
