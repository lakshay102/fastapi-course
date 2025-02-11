from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()

@app.get("/")
def root():
    return{"message" : "Hello world"}

@app.get("/posts")
def read_posts():
    return{"message" : "This is your posts"}

@app.post("/createposts")
def create_post(payLoad: dict = Body(...)):
    print(payLoad)
    return{"message" : f"title : {payLoad['title']} ,content : {payLoad['content']}"}