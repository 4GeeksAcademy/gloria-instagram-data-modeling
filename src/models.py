import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Enum, Table
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(250), nullable=False)
    firstname = Column(String(250))
    lastname = Column(String(250))
    email = Column(String(250), unique=True, nullable=False)

    # Relationships
    followers = relationship('Follower', back_populates='user_to', foreign_keys='Follower.user_to_id')
    following = relationship('Follower', back_populates='user_from', foreign_keys='Follower.user_from_id')
    posts = relationship('Post', back_populates='user')

class Follower(Base):
    __tablename__ = 'follower'
    user_from_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    user_to_id = Column(Integer, ForeignKey('user.id'), primary_key=True)

    # Relationships
    user_from = relationship('User', foreign_keys=[user_from_id], back_populates='following')
    user_to = relationship('User', foreign_keys=[user_to_id], back_populates='followers')

class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    # Relationships
    user = relationship('User', back_populates='posts')
    comments = relationship('Comment', back_populates='post')
    media = relationship('Media', back_populates='post')

class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    comment_text = Column(String(500), nullable=False)
    author_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)

    # Relationships
    post = relationship('Post', back_populates='comments')
    author = relationship('User')

class Media(Base):
    __tablename__ = 'media'
    id = Column(Integer, primary_key=True)
    type = Column(Enum('image', 'video', name='media_type'), nullable=False)
    url = Column(String(500), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)

    # Relationships
    post = relationship('Post', back_populates='media')

# Draw from SQLAlchemy base
try:
    result = render_er(Base, 'instagram_diagram.png')
    print("Success! Check the instagram_diagram.png file")
except Exception as e:
    print("There was a problem generating the diagram")
    raise e
