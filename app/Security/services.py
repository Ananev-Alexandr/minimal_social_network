from datetime import datetime, timedelta
from typing import Union

from database import crud, models
from database.db import SessionLocal
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from Security.schemas import *
from sqlalchemy.orm import Session

from .constants import *

# to get a string like this run:
# openssl rand -hex 32


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

    
def login(db: Session, username: str, password: str):
    db_user = db.query(models.User).\
        filter(models.User.login == username).one_or_none()
    db_user_with_pass = db_user.password
    hash_pass = crud.verify_password(password, str(db_user_with_pass))
    if db_user and hash_pass:
        return db_user
    raise HTTPException(status_code=401, detail="Login or password is wrong")


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = crud.info_about_user_for_login(db=db, login=token_data.username)
    if user is None:
        raise credentials_exception
    return user
    