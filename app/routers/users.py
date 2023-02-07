from fastapi import APIRouter, Depends
from database import crud, models, schemas
from sqlalchemy.orm import Session
from database.db import SessionLocal, engine
from typing import Union

# создание таблицы в БД
models.Base.metadata.create_all(bind=engine)


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
async def hello():
    return {"Hello": "World"}


@router.post("/users/", response_model=schemas.UserOut)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)


@router.get("/users/{id}", response_model=Union[schemas.UserOut, None])
async def info_about_user(id: int, db: Session = Depends(get_db)):
    return crud.info_about_user(id=id, db=db)


@router.post("/login/")
async def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    return crud.login(db=db, user=user)


@router.post("/logout/")
async def logout():
    return crud.logout()