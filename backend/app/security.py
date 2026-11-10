from datetime import datetime,timedelta,timezone
from jose import jwt,JWTError
from pwdlib import PasswordHash
from .config import settings
_hasher=PasswordHash.recommended()
def hash_password(password:str)->str: return _hasher.hash(password)
def verify_password(password:str,hashed:str)->bool: return _hasher.verify(password,hashed)
def create_access_token(user_id:str)->str:
    exp=datetime.now(timezone.utc)+timedelta(minutes=settings.access_token_minutes)
    return jwt.encode({'sub':user_id,'exp':exp},settings.jwt_secret,algorithm=settings.jwt_algorithm)
def decode_access_token(token:str):
    try: return jwt.decode(token,settings.jwt_secret,algorithms=[settings.jwt_algorithm]).get('sub')
    except JWTError: return None
