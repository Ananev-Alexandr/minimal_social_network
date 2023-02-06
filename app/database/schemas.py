from pydantic import BaseModel


class UserBase(BaseModel):
    login: str


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