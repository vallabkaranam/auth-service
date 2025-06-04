from datetime import datetime, timezone, timedelta
import os
from dotenv import load_dotenv
from fastapi import HTTPException
from jose import jwt

load_dotenv()

# JWT configuration loaded from environment variables
ACCESS_TOKEN_SECRET_KEY = os.getenv("ACCESS_TOKEN_SECRET_KEY")
REFRESH_TOKEN_SECRET_KEY = os.getenv("REFRESH_TOKEN_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES")
JWT_REFRESH_TOKEN_EXPIRE_DAYS = os.getenv("JWT_REFRESH_TOKEN_EXPIRE_DAYS")

def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    Creates a short-lived JWT access token for API authentication.
    
    Args:
        data (dict): Payload data to encode in the token (typically user info)
        expires_delta (timedelta, optional): Custom expiration time. Defaults to JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        
    Returns:
        tuple: (encoded_jwt, issued_at_timestamp, expiration_timestamp)
    """
    to_encode = data.copy()
    iat = datetime.now(timezone.utc)
    expire = iat + (expires_delta or timedelta(minutes=int(JWT_ACCESS_TOKEN_EXPIRE_MINUTES)))
    to_encode.update({"exp": expire})
    to_encode.update({"iat": iat})
    encoded_jwt = jwt.encode(to_encode, ACCESS_TOKEN_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt, iat, expire

def create_refresh_token(data: dict, expires_delta: timedelta = None):
    """
    Creates a long-lived JWT refresh token for obtaining new access tokens.
    
    Args:
        data (dict): Payload data to encode in the token (typically user info)
        expires_delta (timedelta, optional): Custom expiration time. Defaults to JWT_REFRESH_TOKEN_EXPIRE_DAYS
        
    Returns:
        tuple: (encoded_jwt, issued_at_timestamp, expiration_timestamp)
    """
    to_encode = data.copy()
    iat = datetime.now(timezone.utc)
    expire = iat + (expires_delta or timedelta(minutes=int(JWT_REFRESH_TOKEN_EXPIRE_DAYS)))
    to_encode.update({"exp": expire})
    to_encode.update({"iat": iat})
    encoded_jwt = jwt.encode(to_encode, REFRESH_TOKEN_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt, iat, expire

def decode_refresh_token(refresh_token: str):
    """
    Decodes and validates a refresh token.
    
    Args:
        refresh_token (str): The refresh token to decode
        
    Returns:
        dict: The decoded token payload
        
    Raises:
        HTTPException: If token is invalid or expired
    """
    payload = jwt.decode(refresh_token, REFRESH_TOKEN_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    return payload
    

