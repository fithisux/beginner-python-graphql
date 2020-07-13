# Imports
from flask import Flask# app initialization
from sqlalchemy import *
from sqlalchemy.orm import (scoped_session, sessionmaker, relationship,
                            backref)
import os
from flaskql.models import Base 
from flaskql import schema
from flask_graphql import GraphQLView
import graphene

def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="dev",
        # store the database in the instance folder
        DATABASE=os.path.join(app.instance_path, "flaskql.sqlite"),
    )
    
    app.debug = True

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    print(app.config['DATABASE'])
    
    from flaskql import db

    db.init_app(app)
    
    gschema = graphene.Schema(query=schema.Query, mutation=schema.Mutation)
    
    app.add_url_rule(
        '/graphql', view_func=GraphQLView.as_view('graphql', schema=gschema, graphiql=True)
    )
    return app
