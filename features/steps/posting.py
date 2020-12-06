from behave import given, when, then

import requests
import json


@given('We are in the initial state')
def is_initialized(context):
    query = '''
        {
            allposts { 
                title 
                user {
                        id
                    } 
                } 
        }
    '''
    json_body = {'query' : query}
    headers = {'Content-Type': 'application/json'}
    rv = requests.post(url='http://127.0.0.1:5000/graphql', json=json_body, headers=headers)
    expected_json_response = '{"data":{"allposts":[{"title":"Flowers","user":{"id":1}}]}}'
    assertion_helper(rv.text, expected_json_response)

    
@when('A post is created with data')
def post_creation(context):
    row = context.table[0]
    body = row['body']
    title = row['title']
    userid = int(row['userid'])
    query = '''
        mutation postCreator($body: String!, $title: String!, $userId: Int!){ 
            createPost(body: $body, title: $title, userId: $userId) { 
                post { 
                        body 
                        title 
                        user { id } 
                } 
                ok 
            } 
        }
    '''
    
    variables =  json.dumps({'body': body, 'title': title, 'userId': userid})

    
    json_body = {'query' : query, 'variables': variables}
    headers = {'Content-Type': 'application/json'}
    rv = requests.post(url='http://127.0.0.1:5000/graphql', json=json_body, headers=headers)
    expected_json_response = {
        'data':{
            'createPost':{
                'post':{'body':body,'title':title,'user':{'id':userid}},
                'ok': True
                }
            }
        }
    assertion_helper(json.dumps(json.loads(rv.text)), json.dumps(expected_json_response))

@then('We can retrieve only one post with data')
def post_asserton(context):
    row = context.table[0]
    body = row['body']
    title = row['title']
    userid = int(row['userid'])
    query = '''
        {
            allposts { 
                title 
                body
                user {
                        id
                    } 
                } 
        }
    '''
    json_body = {'query' : query}
    headers = {'Content-Type': 'application/json'}
    rv = requests.post(url='http://127.0.0.1:5000/graphql', json=json_body, headers=headers)
    expected_json_response = {
        'data': {
            'allposts': [
                {'title': "Flowers", 'body': "A rose is a rose", 'user': {'id': 1}},
                {'title': title, 'body': body, 'user': {'id': userid}}]
            }
        }
    assertion_helper(json.dumps(json.loads(rv.text)), json.dumps(expected_json_response))
    
    
def assertion_helper(real_HS, expected_HS):
    assert real_HS == expected_HS, f"Expected {expected_HS} but got {real_HS} instead"