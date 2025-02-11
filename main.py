from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_posts = [
    {"title": "Title of post 1", "content": "Content of post 1", "id": 1},
    {"title": "Favorite singer", "content": "Weekend", "id": 2},
]


def find_post(id):
    for post in my_posts:
        if id == post["id"]:
            return post


@app.get("/")
def root():
    return {"message": "Hello world"}


@app.get("/posts")
def read_posts():
    return {"data": my_posts}


@app.post("/posts", status_code= status.HTTP_201_CREATED)
def create_post(post: Post):
    # print(post)
    # print(post.model_dump())
    post_dict = post.model_dump()
    my_posts.append(post_dict)
    return {"data": post_dict}


@app.get("/posts/latest")
def get_latest_post():
    latest_post = my_posts[len(my_posts) - 1]
    return {"detail": latest_post}


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message" : f"post with id: {id} was not found"}
    # print(type(id))
    return {"post_detail": post}
