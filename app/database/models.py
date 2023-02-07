from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .db import Base

# class User(Base):
#     __tablename__ = "user_table"

#     id = Column(Integer, primary_key=True)
#     login = Column(String, unique=True, nullable=False)
#     password = Column(String, nullable=False)
#     first_name = Column(String)
#     second_name = Column(String)
    
#     posts = relationship("Post", back_populates="users")


# class Post(Base):
#     __tablename__ = "post_table"

#     id = Column(Integer, primary_key=True, index=True, autoincrement=True)
#     id_user = Column(Integer, ForeignKey("user_table.id"), nullable=False)
#     content = Column(String, nullable=False)
#     publication_date = Column(DateTime, default=datetime.now)
    
#     users = relationship("User", back_populates="posts")
#     likes = relationship("LikePost", back_populates="posts")
    
    
# class LikePost(Base):
#     __tablename__ = "like_table"
    
#     id = Column(Integer, primary_key=True, index=True, autoincrement=True)
#     id_post = Column(Integer, ForeignKey("post_table.id"), nullable=False)
    
#     posts = relationship("Post", back_populates="likes")


# class Association(Base):
#     __tablename__ = "association_table"
#     user_id = Column(ForeignKey("user_table.id"), primary_key=True)
#     post_id = Column(ForeignKey("post_table.id"), primary_key=True)

#     posts = relationship("Post", back_populates="users")
#     users = relationship("User", back_populates="posts")
    
class LikePost(Base):
    __tablename__ = "like_table"
    
    post_id = Column(ForeignKey("post_table.id"), nullable=False, primary_key=True)
    user_id = Column(ForeignKey("user_table.id"), nullable=False, primary_key=True)

    # posts = relationship("Post", back_populates="users")
    # users = relationship("User", back_populates="posts")
    
    child = relationship("Post", back_populates="parents")
    parent = relationship("User", back_populates="children")
class User(Base):
    __tablename__ = "user_table"

    id = Column(Integer, primary_key=True)
    login = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    first_name = Column(String)
    second_name = Column(String)
    
    # posts = relationship("LikePost", back_populates="users")
    children = relationship("LikePost", back_populates="parent")


class Post(Base):
    __tablename__ = "post_table"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_user = Column(Integer, ForeignKey("user_table.id"), nullable=False)
    content = Column(String, nullable=False)
    publication_date = Column(DateTime, default=datetime.now)
    
    # users = relationship("LikePost", back_populates="posts")
    parents = relationship("LikePost", back_populates="child")