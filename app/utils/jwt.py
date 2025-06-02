from datetime import datetime, timezone, timedelta
import os
from dotenv import load_dotenv
from jose import jwt

load_dotenv()

ACCESS_TOKEN_SECRET_KEY = os.getenv("ACCESS_TOKEN_SECRET_KEY")
REFRESH_TOKEN_SECRET_KEY = os.getenv("REFRESH_TOKEN_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES")
JWT_REFRESH_TOKEN_EXPIRE_DAYS = os.getenv("JWT_REFRESH_TOKEN_EXPIRE_DAYS")

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    iat = datetime.now(timezone.utc)
    expire = iat + (expires_delta or timedelta(minutes=int(JWT_ACCESS_TOKEN_EXPIRE_MINUTES)))
    to_encode.update({"exp": expire})
    to_encode.update({"iat": iat})
    encoded_jwt = jwt.encode(to_encode, ACCESS_TOKEN_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt, iat, expire

def create_refresh_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    iat = datetime.now(timezone.utc)
    expire = iat + (expires_delta or timedelta(minutes=int(JWT_REFRESH_TOKEN_EXPIRE_DAYS)))
    to_encode.update({"exp": expire})
    to_encode.update({"iat": iat})
    encoded_jwt = jwt.encode(to_encode, REFRESH_TOKEN_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt, iat, expire

