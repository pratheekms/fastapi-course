from typing import Optional
from fastapi import FastAPI, Response, status
from fastapi.exceptions import HTTPException
# from fastapi.params import Body
from pydantic import BaseModel
# from random import randrange
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
        conn = psycopg2.connect(host='localhost', database='fastapi',
                                user='postgres', password='postgres1',
                                cursor_factory=RealDictCursor)
        cusror = conn.cursor()
        print('Database connection successful')
        break
    except Exception as error:
        print('conenction failed')
        print("Error:", error)
        time.sleep(2)


my_posts = [{"title": "title of post 1",
             "content": "content of post 1", "id": 1},
            {"title": "title of post 2",
             "content": "content of post 2", "id": 2}
            ]


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


@app.get("/")
async def root():
    return {"message": "Hello World!!"}


@app.get("/posts")
def get_posts():
    cusror.execute("""SELECT * FROM posts """)
    posts = cusror.fetchall()
    return {"message": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cusror.execute("""INSERT INTO posts (title,content,published)
    VALUES(%s, %s, %s) RETURNING * """,
                   (post.title, post.content, post.published))
    new_post = cusror.fetchone()
    conn.commit()

    return {"message": new_post}


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    cusror.execute("""SELECT * FROM posts WHERE id= %s""", (str(id),))
    post = cusror.fetchone()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='not found!!!')
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": "post not found"}
    return {"post details": post}


@app.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cusror.execute(
        """DELETE FROM posts WHERE id= %s returning *""", (str(id),))
    deleted_post = cusror.fetchone()
    conn.commit()
    if deleted_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'id {id} not exits')
    # return {"message": "post deleted"}
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cusror.execute(
        """UPDATE posts SET title=%s,content=%s,published=%s 
        WHERE id= %s returning *""",
        (post.title, post.content, post.published, str(id),))
    updated_post = cusror.fetchone()
    conn.commit()
    if updated_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'id {id} not exits')
    return {"data": updated_post}
