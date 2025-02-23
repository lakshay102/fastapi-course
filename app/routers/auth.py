from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import models
from app.schemas import Token, UserLogin
from app.database import get_db
from app.utils import verify_password
from app.oauth2 import create_access_token

router = APIRouter(
    tags= ['Authentication']
)

@router.post('/login', status_code=status.HTTP_200_OK, response_model= Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(
            status_code= status.HTTP_403_FORBIDDEN,
            detail= f'Invalid credentials'
        )
    
    if not verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code= status.HTTP_403_FORBIDDEN,
            detail= f'Invalid credentials'
        )

    # "create a token"
    # "return a toker"

    access_token = create_access_token(data= {"user_id" : user.id})
    return {"access_token" : access_token, "token_type" : "bearer"}