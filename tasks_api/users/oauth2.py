from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from tasks_api.users import tokens
from tasks_api import constants

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")


def get_current_user(data: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return tokens.verify_token(constants.JWT_SECRET_KEY, constants.ALGORITHM, data, credentials_exception)


def get_current_user_refresh_token(data: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate ACCESS TOKEN",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return tokens.verify_token(constants.JWT_REFRESH_SECRET_KEY, constants.ALGORITHM, data, credentials_exception)
