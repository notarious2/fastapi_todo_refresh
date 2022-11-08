from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm.session import Session
from database import get_db
import crud, auth
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from password_hashing import Hash

router = APIRouter(
    tags = ['auth']
)

@router.post('/login')
def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
   user = authenticate_user(db=db, username=form_data.username, password=form_data.password)
   if not user:
    raise HTTPException(
       	status_code=status.HTTP_401_UNAUTHORIZED,
       	detail="Incorrect email or password",
       	headers={"WWW-Authenticate": "Bearer"},
   	)
   access_token = auth.create_access_token(data={"username": user.username}) 
   return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.user_id,
        "username": user.username
    }


#Authenticate user based on username and password
def authenticate_user(username: str, password: str, db: Session = Depends(get_db)):
    # find user with such username
    user = crud.get_user_by_username(db=db, username=username)
    if not user:
        return False
    # check if passwords match - use hashed_password to check
    if not Hash.verify_hashed_password(plain_password=password, hashed_password=user.password):
        return False
    return user        
