import click
from flask import current_app
from flask import g
from flask.cli import with_appcontext
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
from sqlalchemy.orm import Query
from flaskql.models import dao
from sqlalchemy.orm import scoped_session
from contextlib import contextmanager

def get_db():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    if "engine" not in g:
        g.engine = create_engine(f"sqlite:///{current_app.config['DATABASE']}", convert_unicode=True)

    return g.engine


def close_db(e=None):
    """If this request connected to the database, close the
    connection.
    """
    engine = g.pop("engine", None)


@contextmanager
def grab_session(engine):
    Session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    session = Session()
    yield session
    session.close()
    

def init_db():
    """Clear existing data and create new tables."""
    
    engine = get_db()
    
    from sqlalchemy.schema import MetaData

    metadata : MetaData = dao.metadata

    metadata.create_all(engine)

    with grab_session(engine) as session:
        
        Query(dao.User, session).delete()
        Query(dao.Post, session).delete()
        
        user = dao.User(username = 'vasilis', password = 'pass123')
        session.add(user)
    
        post = dao.Post(title = 'Flowers', body = 'A rose is a rose', created = datetime.datetime.now(), author = user)
        session.add(post) 
    
        session.commit() 


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
