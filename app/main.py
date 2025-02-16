from typing import List
from fastapi import Depends, FastAPI, Response, status, HTTPException
from app import models
from app.schemas import Post, PostCreate, UserOut, UserCreate
from .database import engine, get_db
from sqlalchemy.orm import Session
import psycopg2
from psycopg2.extras import RealDictCursor
import time

models.Base.metadata.create_all(bind = engine)

app = FastAPI()

while True:

    try:
        conn = psycopg2.connect(host = 'localhost', database = 'fastapi', user = 'postgres', password = 'postgres', cursor_factory= RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful!")
        break
    except Exception as error:
        print("Connection to database failed")
        print("Error : ", error)
        time.sleep(2)

my_posts = [
    {"title": "Title of post 1", "content": "Content of post 1", "id": 1},
    {"title": "Favorite singer", "content": "Weekend", "id": 2},
]


def find_post(id):
    for post in my_posts:
        if id == post["id"]:
            return post

def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p['id'] == id:
            return i

@app.get("/")
def root():
    return {"message": "Hello world"}


@app.get("/posts", response_model= List[Post])
def get_posts(db : Session = Depends(get_db)):
    # cursor.execute(
    #     """SELECT * FROM posts"""
    # )
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts


@app.post("/posts", status_code= status.HTTP_201_CREATED, response_model= Post)
def create_post(post: PostCreate, db : Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))

    # new_post = cursor.fetchone()
    # conn.commit()
    # print(post.model_dump())
    # new_post = models.Post(title = post.title, content = post.content, published = post.published)
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get("/posts/latest")
def get_latest_post():
    latest_post = my_posts[len(my_posts) - 1]
    return latest_post


@app.get("/posts/{id}", response_model= Post)
def get_post(id: int, db : Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    # fetched_post_data = cursor.fetchone()

    fetched_post_data = db.query(models.Post).filter(models.Post.id == id).first()
    if not fetched_post_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )
    return fetched_post_data

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""DELETE from posts WHERE id = %s RETURNING *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Posts with id: {id} does not exist")
    
    post.delete(synchronize_session= False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}",response_model= Post)
def update_post(id : int, post: PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = post_query.first()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Posts with id: {id} does not exist")
    
    post_query.update(post.model_dump(), synchronize_session= False)
    db.commit()
    return post_query.first()

@app.post("/users",status_code= status.HTTP_201_CREATED, response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user