from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from database import Base
from sqlalchemy.orm import relationship


class SubTask(Base):
    __tablename__ = 'sub_tasks'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    details = Column(String)
    date_time = Column(DateTime)
    created_on = Column(DateTime, default=datetime.utcnow)
    starred = Column(Boolean, default=False)
    task_id = Column(Integer, ForeignKey('tasks.id', ondelete="CASCADE"))

    task = relationship("Task", back_populates="sub_task")
