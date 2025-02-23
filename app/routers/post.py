from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Response, status
from app import models
from app.database import get_db
from app.oauth2 import get_current_user
from app.schemas import Post, PostCreate
from sqlalchemy.orm import Session

router = APIRouter(
    prefix= "/posts",
    tags= ['Posts']
)

@router.get("/", response_model= List[Post])
def get_posts(db : Session = Depends(get_db), current_user: int = Depends(get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # cursor.execute(
    #     """SELECT * FROM posts"""
    # )
    # posts = cursor.fetchall()

    # TO fetch all posts for a specific user
    # posts = db.query(models.Post).filter(current_user.id == models.Post.owner_id).all()
    print(search)
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts


@router.post("/", status_code= status.HTTP_201_CREATED, response_model= Post)
def create_post(post: PostCreate, db : Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))

    # new_post = cursor.fetchone()
    # conn.commit()
    # print(post.model_dump())
    # new_post = models.Post(title = post.title, content = post.content, published = post.published)
    owner_id = current_user.id
    new_post = models.Post(owner_id = owner_id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}", response_model= Post)
def get_post(id: int, db : Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    # fetched_post_data = cursor.fetchone()

    fetched_post_data = db.query(models.Post).filter(models.Post.id == id).first()
    if not fetched_post_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )
    
    # Fetch used id specific post

    # if fetched_post_data.owner_id != current_user.id:
    #     raise HTTPException(
    #         status_code= status.HTTP_403_FORBIDDEN,
    #         detail= f"Not authorized to perform requested action"
    #     )

    return fetched_post_data

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    # cursor.execute("""DELETE from posts WHERE id = %s RETURNING *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Posts with id: {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= f"Not authorized to perform requested action")
    
    post_query.delete(synchronize_session= False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model= Post)
def update_post(id : int, post: PostCreate, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = post_query.first()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Posts with id: {id} does not exist")
    
    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= f"Not authorized to perform requested action")
    
    post_query.update(post.model_dump(), synchronize_session= False)
    db.commit()
    return post_query.first()