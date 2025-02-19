from fastapi import Depends, HTTPException, status, APIRouter
from app import models
from app.database import get_db
from app.schemas import UserCreate, UserOut
from app.utils import hash_password_generator
from sqlalchemy.orm import Session

router = APIRouter(
    prefix= "/users",
    tags= ['Users']
)

@router.post("/",status_code= status.HTTP_201_CREATED, response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    # hash the password - user.password
    hashed_password = hash_password_generator(user.password)
    user.password = hashed_password

    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}", response_model= UserOut)
def get_users(id:int, db: Session = Depends(get_db)):
    fetched_user_data = db.query(models.User).filter(models.User.id == id).first()
    if not fetched_user_data:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= f"User with id: {id} was not found"
        )
    
    return fetched_user_data