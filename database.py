import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# Load the database URL from the environment variable
db_url = os.environ.get('DB_URL')

# Create the SQLAlchemy engine
engine = create_engine(db_url, echo=True)

# Create the sessionmaker object
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Define the declarative base
Base = declarative_base()


def get_db():
    """
    This method is used to create the database instance.
    :return: database instance
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
