from datetime import datetime, timedelta
from jose import JWTError, jwt
from tasks_api.users import schemas


def create_token(secret_key, algorithm, token_expire_min, data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=token_expire_min)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt


def verify_token(secret_key, algorithm, token: str, credentials_exception):
    try:
        payload = jwt.decode(token, secret_key, algorithms=algorithm)
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
        return token_data
    except JWTError:
        raise credentials_exception
