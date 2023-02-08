from fastapi import APIRouter, Depends
from database import crud, models, schemas
from sqlalchemy.orm import Session
from database.db import SessionLocal, engine
from Security import services


models.Base.metadata.create_all(bind=engine)


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/post/", response_model=schemas.PostDB)
async def create_post(post: schemas.PostIn, db: Session = Depends(get_db), security = Depends(services.get_current_user)):
    return crud.create_post(db=db, post=post, id_user=security.id)


@router.get("/post/{id}/", response_model=schemas.PostDB)
async def info_about_post(id: int, db: Session = Depends(get_db), security = Depends(services.get_current_user)):
    return crud.info_about_post(id=id, db=db)


@router.get("/like/")
async def like_post(id: int, db: Session = Depends(get_db), security = Depends(services.get_current_user)):
    return crud.like_post(id=id, user_id=security.id, db=db)
