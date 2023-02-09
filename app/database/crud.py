from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models, schemas
from datetime import datetime

from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    eq_pass = pwd_context.verify(plain_password, hashed_password)
    return eq_pass


def get_password_hash(password):
    hash = pwd_context.hash(password)
    return hash


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        password=get_password_hash(user.password),
        first_name=user.first_name,
        second_name=user.second_name,
        login=user.login
    )
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except:
        raise HTTPException(status_code=404, detail="This username already exists, please use another one")


def info_about_user(db: Session, id: int):
    db_user = db.query(models.User).\
        filter(models.User.id == id).one_or_none()
    if db_user:
        return db_user
    raise HTTPException(status_code=404, detail="Id not found")


def info_about_user_for_login(db: Session, login: str):
    db_user = db.query(models.User).\
        filter(models.User.login == login).one_or_none()
    if db_user:
        return db_user


def login(db: Session, user: schemas.UserLogin):
    db_user = db.query(models.User).\
        filter(models.User.login == user.login).one_or_none()
    db_user_with_pass = db_user.password
    hash_pass = verify_password(user.password, str(db_user_with_pass))
    if db_user and hash_pass:
        return {"message": "Success"}
    raise HTTPException(status_code=401, detail="Login or password is wrong")


def logout():
    user_is_auth = 0
    if user_is_auth:
        return {"message": "Success logout"}
    raise HTTPException(status_code=404, detail="You are not login!")


def create_post(db: Session, post: schemas.PostIn, id_user: int):
    db_post = models.Post(
        id_user=id_user,
        content=post.content,
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def info_about_post(id: int, db: Session):
    get_post = db.query(models.Post).\
        filter(models.Post.id == id).one_or_none()
    if get_post:
        return get_post
    raise HTTPException(status_code=404, detail="Id not found")


def like_post(id: int, user_id: int, db: Session):
    find_post_like = db.query(models.LikePost).\
        filter(models.LikePost.post_id == id,\
            models.LikePost.user_id == user_id).one_or_none()
    get_post = db.query(models.Post).\
        filter(models.Post.id == id, models.Post.id_user == user_id).one_or_none()
    if get_post:
        raise HTTPException(status_code=400, detail="You cannot like this post")
    elif find_post_like:
        db.delete(find_post_like)
        db.commit()
        return {"message": "You delete like"}
    else:
        like_post_id = models.LikePost(
            post_id=id,
            user_id=user_id
        )
        db.add(like_post_id)
        db.commit()
        db.refresh(like_post_id)
        return {"message": "You like it"}
    

def change_post(id: int, user_id: int, new_content: str, db: Session):
    find_post = db.query(models.Post).\
        filter(models.Post.id == id,\
            models.Post.id_user == user_id).one_or_none()
    if find_post:
        db.query(models.Post).filter(models.Post.id == id)\
            .update({models.Post.content: new_content, models.Post.publication_date: datetime.now()})
        db.commit()
        return find_post
    else:
        raise HTTPException(status_code=400, detail="Its not your post")

