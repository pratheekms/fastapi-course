from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World!!"}

@app.get("/post")
def get_post():
    return {"message": "posts are here"}

@app.post("/createposts")
def create_posts(payload: dict=Body(...)):
    print(payload)
    print(payload["desc"])
    return {"message":f"titlle {payload['tittle']}"}
