from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jose import jwt, JWTError
from app.core.config import settings
pwd=CryptContext(schemes=["argon2"], deprecated="auto")
def hash_password(value): return pwd.hash(value)
def verify_password(value, hashed): return pwd.verify(value, hashed)
def create_token(subject, minutes=None):
    return jwt.encode({"sub":subject,"exp":datetime.now(timezone.utc)+timedelta(minutes=minutes or settings.access_token_minutes)}, settings.jwt_secret, algorithm="HS256")
def decode_token(token): return jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
