from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm.session import Session
from database import get_db
import crud
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from password_hashing import Hash
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder
import datetime
expires = datetime.timedelta(seconds=5)
router = APIRouter(
    tags = ['auth']
)

@router.post('/login')
async def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends(), Authorize: AuthJWT = Depends()):
   """
    ## LogIn a User
    This requires the following fields:
    ```
        username: str
        password: str

    and returns a token pair 'access' and 'refresh'
    ```
        
   """ 
   user = authenticate_user(db=db, username=form_data.username, password=form_data.password)
    
   print("USER:", user)
   if not user:
    raise HTTPException(
       	status_code=status.HTTP_401_UNAUTHORIZED,
       	detail="Incorrect email or password",
       	headers={"WWW-Authenticate": "Bearer"},
   	)
   access_token = Authorize.create_access_token(subject = user.username, expires_time=expires)
   refresh_token = Authorize.create_refresh_token(subject = user.username)
    
   print(access_token)
    
   response = {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user_id": user.user_id,
        "username": user.username
    }
   
   return jsonable_encoder(response) 

@router.get('/refresh')
def refresh(Authorize: AuthJWT = Depends()):
    Authorize.jwt_refresh_token_required()
    current_user = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject=current_user,expires_time=expires)
    return {"access_token": new_access_token}


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
