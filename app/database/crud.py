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


def find_post(db: Session, schemas_filter: schemas.FilteredPosts):
    schemas_filter, group_filters = validate_params(schemas_filter)
    result = filter_posts(db.query(models.Post), schemas_filter)
    result = sort_post(result, group_filters)
    return result.all()
   
   
def filter_posts(query, dict_of_filter):
    association_table = {
        "id": models.Post.id,
        "content": models.Post.content,
        "publication_date": models.Post.publication_date,
        # "first_name": models.Post.content,
        # "second_name": models.Post.content
    }

    for key, val in dict_of_filter.items():
        if key == "id":
            query = query.filter(association_table[key] == val)
        elif key == "content":
            query = query.filter(association_table[key].ilike(f'%{val}%'))
        elif key == "publication_date":
            date_range = dict(val)
            if date_range.get("start_date"):
                query = query.filter(association_table[key] >= date_range["start_date"])
            if date_range.get("end_date"):
                query = query.filter(association_table[key] <= date_range["end_date"])
    return query
       
 
 
def validate_params(dict_of_filter):
    dict_of_filter = dict(dict_of_filter)
    if dict_of_filter.get("filters"):
        dict_filters = dict(dict_of_filter.get("filters"))
    if dict_of_filter.get("group"):
        group_filters = dict(dict_of_filter["group"])
    if dict_filters.get("publication_date"):
        dict_filters["publication_date"] = dict(dict_filters["publication_date"])

    copy_filters = dict_filters.copy()
    for key, val in copy_filters.items():
        if val is None:
            del dict_filters[key]
                
    return dict_filters, group_filters
    
def sort_post(query, group_filters: dict):
    from sqlalchemy import desc, asc
    association_table = {
        "id": models.Post.id,
        "content": models.Post.content,
        "publication_date": models.Post.publication_date,
    }
    sort_table = {
        "asc": asc,
        "desc": desc
    }
    asc_or_desc = sort_table.get(group_filters.get("group_by"))
    db_column = association_table.get(group_filters.get("sort_by"))
    query = query.order_by(asc_or_desc(db_column))
    
    return query 


def paginate():
    # TODO
    pass


def like_post(id: int, user_id: int, db: Session):
    find_post_like = db.query(models.LikePost).\
        filter(models.LikePost.post_id == id,\
            models.LikePost.user_id == user_id).one_or_none()
    get_post = db.query(models.Post).\
        filter(models.Post.id == id, models.Post.id_user == user_id).one_or_none()
    if get_post:
        raise HTTPException(status_code=403, detail="You cannot like this post")
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
        raise HTTPException(status_code=403, detail="Its not your post, post not found")


def delete_post(id: int, user_id: int, db: Session):
    find_post = db.query(models.Post).\
        filter(models.Post.id == id,\
            models.Post.id_user == user_id).one_or_none()
    if find_post:
        post = db.query(models.Post).filter(models.Post.id == id).first()
        like_post = db.query(models.LikePost).filter(models.LikePost.post_id == id).all()
        db.delete(post)
        for like in like_post:
            db.delete(like)
        db.commit()
        return {"message": "Success delete!"}
    else:
        raise HTTPException(status_code=403, detail="Its not your post, post not found")