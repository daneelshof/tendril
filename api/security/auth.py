from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Security
from datetime import datetime, timedelta
from typing import Any, Union
from jose import jwt


class AuthHander():
    security = HTTPBearer()
    algorithm = 'HS256'
    secret_key = 'test'
    token_expire_minutes = 300

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=self.algorithm)
            return payload['sub']
        except jwt.ExpiredSignatureError:
            raise RequiresLoginException()
        except jwt.JWTError as e:
            raise RequiresLoginException()
        except Exception as e:
            raise RequiresLoginException()

    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_token(auth.credentials)

    def create_access_token(self,
                           subject: Union[str, Any],
                           expires_delta: timedelta = None) -> str:
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=self.token_expire_minutes
            )

        to_encode = {"exp": expire, "sub": str(subject)}
        encoded_jwt = jwt.decode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def get_hash_password(self, password, salt, iterations):
        pass

    def verify_password(self, password, hashed_password, salt, iterations):
        pass

    async def authenticate_user(self, username, password):
        try:
            # Lookup user in DB
            # check password
            return True
        except:
            raise RequiresLoginException()


class RequiresLoginException(Exception):
    pass