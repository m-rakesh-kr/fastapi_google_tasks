from pydantic import BaseModel
from datetime import datetime


class BaseTask(BaseModel):
    title: str
    details: str
    date_time: datetime


class Task(BaseModel):
    title: str
    details: str
    date_time: datetime

    class Config:
        orm_mode = True


class ShowTask(BaseModel):
    id: str
    title: str
    details: str
    date_time: datetime
    list_id: str

    class Config:
        orm_mode = True
