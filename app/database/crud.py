from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models, schemas

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
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def login(db: Session, user: schemas.UserLogin):
    db_user = db.query(models.User).\
        filter(models.User.login == user.login).one_or_none()
    db_user_with_pass = db_user.password
    hash_pass = verify_password(user.password, str(db_user_with_pass))
    if db_user and hash_pass:
        return {"message": "Success"}
    # return {"message": "Login or password is wrong"}
    raise HTTPException(status_code=401, detail="Login or password is wrong")

def logout():
    # user_is_auth = "pass"
    user_is_auth = 0
    if user_is_auth:
        return {"message": "Success logout"}
    raise HTTPException(status_code=404, detail="You are not login!")