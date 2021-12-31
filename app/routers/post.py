
from fastapi import Response, HTTPException, status, Depends, APIRouter
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List
import psycopg2
from psycopg2.extras import RealDictCursor
import time

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

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


@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    # cusror.execute("""SELECT * FROM posts """)
    # posts = cusror.fetchall()
    posts = db.query(models.Post).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED,
             response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    # cusror.execute("""INSERT INTO posts (title,content,published)
    # VALUES(%s, %s, %s) RETURNING * """,
    #                (post.title, post.content, post.published))
    # new_post = cusror.fetchone()
    # conn.commit()
    
    new_post = models.Post(owner_id=current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, response: Response, db: Session = Depends(get_db),
             current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    # cusror.execute("""SELECT * FROM posts WHERE id= %s""", (str(id),))
    # post = cusror.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='not found!!!')
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": "post not found"}
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),
                current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    # cusror.execute(
    #     """DELETE FROM posts WHERE id= %s returning *""", (str(id),))
    # deleted_post = cusror.fetchone()
    # conn.commit()
    deleted_post_query = db.query(models.Post).filter(models.Post.id == id)
    deleted_post=deleted_post_query.first()
    if deleted_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'id {id} not exits')
    # return {"message": "post deleted"}
    if deleted_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorised")

    deleted_post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate,
                db: Session = Depends(get_db),
                current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    # cusror.execute(
    #     """UPDATE posts SET title=%s,content=%s,published=%s
    #     WHERE id= %s returning *""",
    #     (post.title, post.content, post.published, str(id),))
    # updated_post = cusror.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'id {id} not exits')
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorised")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
