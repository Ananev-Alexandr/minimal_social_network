from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .db import Base


class LikePost(Base):
    __tablename__ = "like_table"
    
    post_id = Column(ForeignKey("post_table.id"), nullable=False, primary_key=True)
    user_id = Column(ForeignKey("user_table.id"), nullable=False, primary_key=True)
    
    child = relationship("Post", back_populates="parents")
    parent = relationship("User", back_populates="children")


class User(Base):
    __tablename__ = "user_table"

    id = Column(Integer, primary_key=True)
    login = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    first_name = Column(String)
    second_name = Column(String)

    children = relationship("LikePost", back_populates="parent")


class Post(Base):
    __tablename__ = "post_table"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_user = Column(Integer, ForeignKey("user_table.id"), nullable=False)
    content = Column(String, nullable=False)
    publication_date = Column(DateTime, default=datetime.now)
    
    parents = relationship("LikePost", back_populates="child")