from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Response, status
from app import models
from app.database import get_db
from app.oauth2 import get_current_user
from app.schemas import Post, PostCreate, Vote
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

@router.post("/",status_code= status.HTTP_201_CREATED)
def vote(vote: Vote, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):

    vote_query = db.query(models.Vote).filter(models.Vote.user_id == current_user.id, models.Vote.post_id == vote.post_id)

    found_vote = vote_query.first()
    if(vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code= status.HTTP_409_CONFLICT, detail= f"user {current_user.id} has already voted on post {vote.post_id}")
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return{"message" : "successfully added vote"}
    
    else:
        if not found_vote:
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"Vote does not exist")
        
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message" : "successfully deleted vote"}