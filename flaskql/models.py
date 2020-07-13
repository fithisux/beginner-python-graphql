from sqlalchemy import *
from sqlalchemy.orm import (scoped_session, sessionmaker, relationship,
                            backref)
from sqlalchemy.ext.declarative import declarative_base
from typing import Any

Base : Any = declarative_base()
print(Base.metadata)

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique = True, nullable=False)
    password = Column(String, nullable=False)


class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    
    title = Column(String, nullable=False)
    body = Column(String, nullable=False)
    
    created = Column(TIMESTAMP, default=func.now())
    
    author_id = Column(Integer, ForeignKey('user.id'))
    author = relationship(
        User,
        backref=backref('posts',
                        uselist=True,
                        cascade='delete,all'))