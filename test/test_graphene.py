from collections import OrderedDict 
from graphene.test import Client
from flaskql.schema import query
from flaskql.schema import mutation
import graphene
import pytest
import flaskql
import os
import tempfile


@pytest.fixture
def my_app_context():
    db_fd, db_fname = tempfile.mkstemp()
    test_config = {
        'DATABASE': db_fname,
        'TESTING': True
    }

    test_app = flaskql.create_app(test_config)
    with test_app.app_context() as app_context:
        flaskql.db.init_db()
        yield app_context
        

    os.close(db_fd)
    os.unlink(db_fname)
    
gschema = graphene.Schema(query=query.Query, mutation=mutation.Mutation)

def test_initial_state(my_app_context):
    client = Client(gschema)
    executed = client.execute('''
    {
      allposts {
        title
        user {
          id
        }
      }
    }
    ''')
    assert executed == {'data': {'allposts': [{'title': 'Flowers', 'user': {'id': 1}}]}}
    
def test_create_post(my_app_context):
    client = Client(gschema)
    variables = {
        "body" : "A sky is nice",
        "title" : "Sunday",
        "userId": 1 
    }
    executed = client.execute('''
     mutation postCreator($body: String!, $title: String!, $userId: Int!){
          createPost(body: $body, title: $title, userId: $userId) {
            post {
              body
              title
              user {
                  id
              }
            }
            ok
          }
        }
    ''',None, None, variables)
    assert executed == {
        "data": {
            "createPost": {
                "post": {
                    "body": "A sky is nice",
                    "title": "Sunday",
                    "user": {
                        "id": 1
                    }
                },
                "ok": True
            }
        }
    }