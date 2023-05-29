
from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from database import Base
from sqlalchemy.orm import relationship


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    details = Column(String)
    date_time = Column(DateTime)
    created_on = Column(DateTime, default=datetime.utcnow)
    starred = Column(Boolean, default=False)
    list_id = Column(Integer, ForeignKey('task_lists.id', ondelete="CASCADE"))

    list = relationship("TaskList", back_populates="task")
    sub_task = relationship('SubTask', back_populates="task", cascade="all, delete")
