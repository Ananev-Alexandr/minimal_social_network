from database import crud, schemas
from database.db_connect import get_db
from fastapi import APIRouter, Depends
from fastapi_pagination import Page, paginate
from Security import services
from sqlalchemy.orm import Session

router = APIRouter(tags=["posts"])


@router.post("/post/", response_model=schemas.PostDB)
async def create_post(
    post: schemas.PostIn,
    db: Session = Depends(get_db),
    security=Depends(services.get_current_user)
        ):
    return crud.create_post(db=db, post=post, id_user=security.id)


@router.get("/post/{id}/", response_model=schemas.PostDB)
async def info_about_post(
    id: int,
    db: Session = Depends(get_db),
    security=Depends(services.get_current_user)
        ):
    return crud.info_about_post(id=id, db=db)


@router.post("/find_post/", response_model=Page[schemas.FilterPostDB])
async def find_post(
    filter: schemas.Asda,
    db: Session = Depends(get_db),
    security=Depends(services.get_current_user)
        ):
    return paginate(crud.find_post(schemas_filter=filter, db=db))


@router.get("/like/")
async def like_post(
    id: int,
    db: Session = Depends(get_db),
    security=Depends(services.get_current_user)
        ):
    return crud.like_post(id=id, user_id=security.id, db=db)


@router.put("/post/{id}/", response_model=schemas.PostDB)
async def change_post(
    id: int,
    new_content: str,
    db: Session = Depends(get_db),
    security=Depends(services.get_current_user)
        ):
    return crud.change_post(
        id=id,
        user_id=security.id,
        new_content=new_content,
        db=db
            )


@router.delete("/post/{id}/")
async def delete_post(
    id: int,
    db: Session = Depends(get_db),
    security=Depends(services.get_current_user)
        ):
    return crud.delete_post(id=id, user_id=security.id, db=db)
