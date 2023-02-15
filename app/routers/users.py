from fastapi import APIRouter, Depends, HTTPException, status
from database import crud, schemas
from sqlalchemy.orm import Session
from typing import Union
from Security import constants, services
from Security.schemas import Token
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from database.db_connect import get_db


router = APIRouter(tags=["users"])


@router.get("/")
async def hello(security = Depends(services.get_current_user)):
    print(security)
    return {"Hello": "World"}


@router.post("/users/", response_model=schemas.UserOut)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)


@router.get("/users/{id}", response_model=Union[schemas.UserOut, None])
async def info_about_user(id: int, db: Session = Depends(get_db), security = Depends(services.get_current_user)):
    return crud.info_about_user(id=id, db=db)


@router.post("/token", response_model=Token, include_in_schema=False)
async def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = services.login(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=constants.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = services.create_access_token(
        data={"sub": user.login}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
