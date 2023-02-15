from pydantic import BaseModel
from datetime import datetime, date
from typing import Union

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
    
    
class DateFilter(BaseModel):
    start_date: Union[date, None] = None
    end_date: Union[date, None] = None




class FilteredPosts(BaseModel):
    id: Union[int, None] = None
    content: Union[str, None] = None
    publication_date: Union[DateFilter, None] = None
    first_name: Union[str, None] = None
    second_name: Union[str, None] = None
        
class SortPost(BaseModel):
    group_by: Union[str, None] = "asc"
    sort_by: Union[str, None] = "id"
    
class Asda(BaseModel):
    filters: Union[FilteredPosts, None] = None
    group: Union[SortPost, None] = None
    
class LikePost(BaseModel):
    post_id: int
    
        
        
class LikePostPath(LikePost):
    user_id: int
    
    
class LikePostDB(LikePost):
    id: int
    user_id: int
    
    class Config:
        orm_mode = True