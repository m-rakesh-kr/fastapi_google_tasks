from sqlalchemy import Column, Integer, String
from database import Base
from sqlalchemy.orm import relationship, Session

import logging

logger = logging.getLogger("fastapi-project")


class User(Base):
    # To change actual table name in the database, As by default it will be same as the model name
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)

    task_list = relationship('TaskList', back_populates="creator", cascade="all, delete")

    @classmethod
    def get_user_by_email(cls, db: Session, email: str):
        return db.query(User).filter(User.email == email).first()
