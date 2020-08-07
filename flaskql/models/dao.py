from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, func
from sqlalchemy.orm import (relationship, backref)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import MetaData

Base = declarative_base()
metadata : MetaData = Base.metadata

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
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))
    
    user = relationship(User, backref=backref("posts", passive_deletes=True))
    