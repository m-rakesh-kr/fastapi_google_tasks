from passlib.context import CryptContext

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hasher:
    """
    Password hashing with Bcrypt.
    https://www.fastapitutorial.com/blog/password-hashing-fastapi/
    """

    @staticmethod
    def bcrypt(password: str):
        return pwd_cxt.hash(password)

    @staticmethod
    def verify(hashed_password, plain_password):
        """
        This method verify the plain password and hashed password.
         param plain_password: plain password
         param hashed_password: hashed password
         return: True if verify else False
        """
        return pwd_cxt.verify(plain_password, hashed_password)
