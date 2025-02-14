from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

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


@app.get("/posts")
def get_posts():
    cursor.execute(
        """SELECT * FROM posts"""
    )
    posts = cursor.fetchall()
    print(posts)
    return {"data": posts}


@app.post("/posts", status_code= status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))

    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}


@app.get("/posts/latest")
def get_latest_post():
    latest_post = my_posts[len(my_posts) - 1]
    return {"detail": latest_post}


@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    fetched_post_data = cursor.fetchone()
    if not fetched_post_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )
    return {"post_detail": fetched_post_data}

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE from posts WHERE id = %s RETURNING *""", (str(id),))
    deleted_post = cursor.fetchone()
    # print(deleted_post)
    conn.commit()

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Posts with id: {id} does not exist")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id : int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    # print(updated_post)
    conn.commit()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Posts with id: {id} does not exist")
    
    return {"data" : updated_post}