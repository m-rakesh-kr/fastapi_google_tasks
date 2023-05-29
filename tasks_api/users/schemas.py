from typing import Optional, List
from pydantic import BaseModel, validator, EmailStr
from .schema_validations import email_validation, password_validation


class UserModel(BaseModel):
    id:str
    name: str
    email: str

    class Config:
        orm_mode = True


class UserRegisterRequest(BaseModel):
    """
       Pydantic models documentation link.
       https://pydantic-docs.helpmanual.io/usage/models/
    """
    name: str
    email: str
    password: str
    confirm_password: str

    # validators
    _email_validator = validator('email', allow_reuse=True)(email_validation)
    _password_validator = validator('password', allow_reuse=True)(password_validation)

    class Config:
        extra = "forbid"


class UserRegisterResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        orm_mode = True


class ShowUser(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        orm_mode = True


class Login(BaseModel):
    username: str
    password: str


class ForgotPassword(BaseModel):
    email: EmailStr


class ResetPassword(BaseModel):
    password: str
    confirm_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    # id: Optional[str] = None
    email: Optional[EmailStr] = None


class EmailSchema(BaseModel):
    email: List[EmailStr]

class UserEmail(BaseModel):
    email: str