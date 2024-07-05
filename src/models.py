import os
import sys
import enum
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er
from sqlalchemy import Enum

Base = declarative_base()

class Type(enum.Enum):
    photo = 'photo'
    video = 'video'
    story = 'story'
    reel = 'reel'
    igtv = 'igtv'
    live = 'live'

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(
        String(64),
        unique=True,
        nullable=False
    )
    firstname = Column(
        String(64),
        unique=False,
        nullable=False
    )
    lastname = Column(
        String(64),
        unique=False,
        nullable=False
    )
    email = Column(
        String(128),
        unique=True,
        nullable=False
    )
    # Relationships
    posts = relationship("Post", back_populates="user", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="author", cascade="all, delete-orphan")
    following = relationship(
        "Follower",
        foreign_keys="[Follower.user_from_id]",
        back_populates="follower",
        cascade="all, delete-orphan"
    )
    followers = relationship(
        "Follower",
        foreign_keys="[Follower.user_to_id]",
        back_populates="followed",
        cascade="all, delete-orphan"
    )
    
class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    # Relationship
    user = relationship("User", back_populates="posts")
    media = relationship("Media", back_populates="post", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")
    
class Media(Base):
    __tablename__ = "media"
    id = Column(Integer, primary_key=True)
    type = Column(Enum(Type), nullable=False)
    url = Column(String(128))
    post_id = Column(Integer, ForeignKey("posts.id"))
    # Relationship
    post = relationship("Post", back_populates="media")
    
class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True)
    comment_text = Column(String(1000), nullable=True)
    author_id = Column(Integer, ForeignKey("users.id"))
    post_id = Column(Integer, ForeignKey("posts.id"))
    # Relationship
    author = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")
    
class Follower(Base):
    __tablename__ = "followers"
    id = Column(Integer, primary_key=True)
    user_from_id = Column(Integer, ForeignKey('users.id'))
    user_to_id = Column(Integer, ForeignKey('users.id'))
    # Relationship
    follower = relationship("User", foreign_keys=[user_from_id], back_populates="following")
    followed = relationship("User", foreign_keys=[user_to_id], back_populates="followers")

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
