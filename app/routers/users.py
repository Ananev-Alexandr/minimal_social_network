from fastapi import APIRouter, Depends
from database import crud, models, schemas
from sqlalchemy.orm import Session
from database.db import SessionLocal, engine

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


@router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)


@router.post("/login/")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    return crud.login(db=db, user=user)


@router.post("/logout/")
def logout():
    return crud.logout()