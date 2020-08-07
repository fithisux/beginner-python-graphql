import click
from flask import current_app
from flask import g
from flask.cli import with_appcontext
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import MetaData
import datetime
from sqlalchemy.orm import Query
from flaskql.models import dao
from sqlalchemy.orm import scoped_session
from contextlib import contextmanager

from sqlalchemy.engine import Engine
from sqlalchemy import event

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
        
def get_engine():
    if "engine" not in g:
        g.engine = create_engine(f"sqlite:///{current_app.config['DATABASE']}", convert_unicode=True)
        metadata : MetaData = dao.metadata
        metadata.create_all(g.engine)
    return g.engine

@contextmanager
def grab_session():
    Session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=get_engine()))
    session = Session()
    yield session
    session.close()
    

def init_db():
    """Clear existing data and create new tables."""
    
    with grab_session() as session:
        
        Query(dao.User, session).delete()
        Query(dao.Post, session).delete()
        
        user = dao.User(username = 'vasilis', password = 'pass123')
        session.add(user)
    
        post = dao.Post(title = 'Flowers', body = 'A rose is a rose', created = datetime.datetime.now(), user = user)
        session.add(post) 
    
        session.commit() 

def close_db(e=None):
    engine = g.pop("engine", None)

@click.command("init-db")
@with_appcontext
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


def init_app(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
