import logging
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Security
from datetime import datetime, timedelta
from typing import Any, Union
from jose import jwt


logger = logging.getLogger(__name__)

class AuthHandler():
    security = HTTPBearer()
    algorithm = 'HS256'
    secret_key = 'test'
    token_expire_minutes = 300

    def decode_token(self, token):
        logger.debug("Entered decode_token")
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=self.algorithm)
            logger.debug(f"Decoded: {payload['sub']}")
            return payload['sub']
        except jwt.ExpiredSignatureError:
            logger.debug("JWT token expired")
            raise RequiresLoginException()
        except jwt.JWTError as e:
            logger.debug("JWT decode error")
            raise RequiresLoginException()
        except Exception as e:
            logger.debug("JWT general exception")
            raise RequiresLoginException()

    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        logger.debug("Entered auth_wrapper")
        return self.decode_token(auth.credentials)

    def create_access_token(self,
                           subject: Union[str, Any],
                           expires_delta: timedelta = None) -> str:
        logger.debug("Entered create_access_token")
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=self.token_expire_minutes
            )

        to_encode = {"exp": expire, "sub": str(subject)}
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def get_hash_password(self, password, salt, iterations):
        pass

    def verify_password(self, password, hashed_password, salt, iterations):
        pass

    async def authenticate_user(self, username, password):
        logger.debug("Entered authenicate_user")
        try:
            if username != "test@test.com":
                return False
            # Lookup user in DB
            # check password
            return True
        except:
            raise RequiresLoginException()


class RequiresLoginException(Exception):
    pass
