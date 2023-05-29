from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from database import Base
from sqlalchemy.orm import relationship


class TaskList(Base):
    __tablename__ = 'task_lists'

    id = Column(Integer, primary_key=True, index=True)
    list_name = Column(String)
    created_on = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"))

    creator = relationship("User", back_populates="task_list")
    task = relationship('Task', back_populates="list", cascade="all, delete")

