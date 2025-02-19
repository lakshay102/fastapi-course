from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models
from app.schemas import UserLogin
from app.database import get_db
from app.utils import verify_password

router = APIRouter(
    tags= ['Authentication']
)

@router.post('/login', status_code=status.HTTP_200_OK)
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()

    if not user:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= f'Invalid credentials'
        )
    
    if not verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= f'Invalid credentials'
        )

    # "create a token"
    # "return a toker"
    return {"token" : "example token"}