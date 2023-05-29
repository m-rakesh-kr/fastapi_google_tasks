import re
from tasks_api import constants
from fastapi import HTTPException, status


def email_validation(email):
    """
    This method validate the user email.
    :param email: user email
    :return: validate email
    """
    regex = constants.EMAIL_REGEX

    if not re.fullmatch(regex, email):
        raise HTTPException(detail=constants.ERR_EMAIL_WRONG, status_code=status.HTTP_401_UNAUTHORIZED)
    else:
        return email


def password_validation(password):
    """
    This method validates the user password according to the regex pattern.
    :param password: user password
    :return: validated password
    """
    regex = constants.PASSWORD_REGEX

    if re.fullmatch(regex, password):
        return password
    else:
        raise HTTPException(detail=constants.ERR_PASSWORD_WRONG, status_code=status.HTTP_401_UNAUTHORIZED,
                            headers={"WWW-Authenticate": constants.PASSWORD_PATTERN_HINT})


def check_confirm_password(password, confirm_password):
    if password != confirm_password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=constants.ERR_PASSWORD_NOT_MATCH)
    else:
        valid_pass = password_validation(password)
        return valid_pass
