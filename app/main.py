from fastapi import FastAPI
from app import models
from app.database import engine
import psycopg2
from psycopg2.extras import RealDictCursor
from app.routers import auth, post, user
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
        
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Hello world"}
