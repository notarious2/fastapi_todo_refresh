from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from fastapi import Depends
import jwt
from fastapi.security import OAuth2PasswordBearer
from config import settings
from datetime import datetime, timedelta
import crud
from database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login") #important path to get token
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = int(settings.ACCESS_TOKEN_EXPIRE_MINUTES)
 
def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(db, token):
  credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
  )
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username: str = payload.get("username")
    if username is None:
      raise credentials_exception
  except jwt.PyJWTError:
    raise credentials_exception
  
  user = crud.get_user_by_username(db, username=username)
  if user is None:
    raise credentials_exception
  return user

def get_current_user(db: Session = Depends(get_db),
                	token: str = Depends(oauth2_scheme)):
   print(token)
   return decode_access_token(db, token)