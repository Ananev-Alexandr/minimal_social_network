from fastapi import APIRouter, Depends
from database import crud, models, schemas
from sqlalchemy.orm import Session
from database.db import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

@router.post("/post/", response_model=schemas.PostDB)
async def create_post(post: schemas.PostIn, db: Session = Depends(get_db)):
    return crud.create_post(db=db, post=post)


@router.get("/post/{id}/", response_model=schemas.PostDB)
async def info_about_post(id: int, db: Session = Depends(get_db)):
    return crud.info_about_post(id=id, db=db)


@router.get("/post/{id}/{user_id}/like")
async def like_post(id: int, user_id: int, db: Session = Depends(get_db)):
    return crud.like_post(id=id, user_id=user_id, db=db)
