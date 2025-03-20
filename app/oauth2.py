from typing import Annotated, Optional
from fastapi import Depends, HTTPException, status
import jwt
from datetime import timedelta, datetime, timezone
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas import TokenData
from app.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl= "token")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp" : expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms= [ALGORITHM])
        id = str(payload.get("user_id"))
        if id is None:
            raise credentials_exception
        # print(id)
        # print(type(id))
        token_data = TokenData(id= id)
    except InvalidTokenError:
        raise credentials_exception
    
    return token_data
    
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code= status.HTTP_401_UNAUTHORIZED,
        detail= f"Could not validate credentials",
        headers= {"WWW-Authenticate" : "Bearer"}
    )

    token = verify_access_token(token, credentials_exception)
    user = db.query(User).filter(User.id == token.id).first()

    return user
