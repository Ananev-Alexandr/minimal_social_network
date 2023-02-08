from pydantic import BaseModel
from datetime import datetime


class UserBase(BaseModel):
    login: str
    
    
class UserOut(BaseModel):
    first_name: str
    second_name: str
    id: int
    
    class Config:
        orm_mode = True


class UserCreate(UserBase):
    first_name: str
    second_name: str
    password: str
    
    
class UserLogin(UserBase):
    password: str
    

class User(UserCreate):
    login: str
    id: int
    
    class Config:
        orm_mode = True
        
        
class PostIn(BaseModel):
    content: str


class PostDB(PostIn):
    id: int
    publication_date: datetime
    
    class Config:
        orm_mode = True
        
        
class LikePost(BaseModel):
    post_id: int
    
        
        
class LikePostPath(LikePost):
    user_id: int
    
    
class LikePostDB(LikePost):
    id: int
    user_id: int
    
    class Config:
        orm_mode = True