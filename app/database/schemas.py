from datetime import date, datetime
from typing import Union

from pydantic import BaseModel


class UserBase(BaseModel):
    login: str


class UserOut(BaseModel):
    first_name: str
    second_name: str
    id: int

    class Config:
        orm_mode = True


class FilterUserOut(BaseModel):
    User: UserOut
    likes_on_the_post: int


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


class FilterUsers(BaseModel):
    first_name: Union[str, None] = None
    second_name: Union[str, None] = None


class SortUsers(BaseModel):
    group_by: Union[str, None] = "asc"
    sort_by: Union[str, None] = "first_name"


class FilterAndSortUsers(BaseModel):
    filters: Union[FilterUsers, None] = None
    group: Union[SortUsers, None] = None


class PostIn(BaseModel):
    content: str


class PostDB(PostIn):
    id: int
    publication_date: datetime

    class Config:
        orm_mode = True


class FilterPostDB(BaseModel):
    Post: PostDB
    User: UserOut
    likes_on_the_post: int

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
    sort_by: Union[str, None] = "publication_date"


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
