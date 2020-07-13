import datetime

import graphene
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.query import Query

from  flaskql import models
from flaskql import db


class GQLUser(graphene.ObjectType):
    username = graphene.String()
    password = graphene.String()
    id = graphene.Int()
    
    @staticmethod
    def convert(user : models.User):
        if user == None :
            return None
        else:
            gqlUser = GQLUser()
            gqlUser.username = user.username
            gqlUser.password = user.password
            gqlUser.id = user.id
            return gqlUser


class GQLPost(graphene.ObjectType):
    title = graphene.String()
    body = graphene.String()
    user = graphene.Field(GQLUser)
    id = graphene.Int()
    created = graphene.DateTime
    
    @staticmethod
    def convert(post : models.Post):
        if post == None :
            return None
        else:
            gqlPost = GQLPost()
            gqlPost.body = post.body
            gqlPost.title = post.title
            gqlPost.id = post.id
            gqlPost.created = post.created
            gqlPost.user = GQLUser.convert(post.author)
            return gqlPost

class CreateUser(graphene.Mutation):
    class Arguments:
        username = graphene.String()
        password = graphene.String()
                
    ok = graphene.Boolean()
    user = graphene.Field(GQLUser)
 
    def mutate(self, info, username=None, password = None):
        print(f"mutate {username} and {password}")
        user = models.User(username=username, password=password)
        Session = sessionmaker(autocommit=False, autoflush=False, bind=db.get_db())
        session = Session()
        session.add(user)
        session.commit()
        ok = True
        return CreateUser(user=GQLUser.convert(user), ok=ok)
     
class CreatePost(graphene.Mutation):
    ok = graphene.Boolean()
    post = graphene.Field(GQLPost)
 
    def mutate(self, info, userId=None, title=None, body=None):
        Session = sessionmaker(autocommit=False, autoflush=False, bind=db.get_db())
        session = Session()
        q = session.query(models.User)
        user = q.filter(models.User.id == userId).one()
         
        if user == None:
            ok= False
            post = None
        else:
            post = models.Post(title = title, body = body , created = datetime.datetime.now(), author = user)
            session.add(user)
            session.commit()
            ok = True
             
        return CreatePost(post=GQLPost.convert(post), ok=ok)
     
class DeleteUser(graphene.Mutation):
    ok = graphene.Boolean()
    user = graphene.Field(GQLUser)
 
    def mutate(self, info, userId=None):
        Session = sessionmaker(autocommit=False, autoflush=False, bind=db.get_db())
        session = Session()
        q = session.query(models.User)
        user = q.filter(models.User.id == userId).one()
         
        if user == None:
            ok= False
        else:
            q.filter(models.User.id == userId).delete()
            ok = True
             
        return DeleteUser(user=GQLUser.convert(user), ok=ok)
     
class DeletePost(graphene.Mutation):
    ok = graphene.Boolean()
    post = graphene.Field(GQLPost)
 

    def mutate(self, info, postId=None):
        Session = sessionmaker(autocommit=False, autoflush=False, bind=db.get_db())
        session = Session()
        q = session.query(models.Post)
        post = q.filter(models.Post.id == postId).one()
         
        if post == None:
            ok= False
        else:
            q.filter(models.Post.id == postId).delete()
            ok = True
             
        return DeletePost(post=GQLPost.convert(post), ok=ok)           
    
class Query(graphene.ObjectType):
    user = graphene.Field(GQLUser, username = graphene.String())
    post = graphene.Field(GQLPost, title = graphene.String())
    allusers = graphene.List(GQLUser) 
    allposts = graphene.List(GQLPost) 
    
    def resolve_user(self, info,  username=None):
        Session = sessionmaker(autocommit=False, autoflush=False, bind=db.get_db())
        session = Session()
        q = session.query(models.User)
        
        return GQLUser.convert(q.filter(models.User.username == username).one())

    def resolve_post(self, info, title=None):    
        Session = sessionmaker(autocommit=False, autoflush=False, bind=db.get_db())
        session = Session()
        q = session.query(models.User)
        
        return GQLPost.convert(q.filter(models.Post.title == title).one())
    
    def resolve_allusers(self, info):
        Session = sessionmaker(autocommit=False, autoflush=False, bind=db.get_db())
        session = Session()
        q = session.query(models.User)

        return [GQLUser.convert(user) for user in q.all()]

    def resolve_allposts(self, info):    
        Session = sessionmaker(autocommit=False, autoflush=False, bind=db.get_db())
        session = Session()
        q = session.query(models.Post)
        
        return [GQLPost.convert(post) for post in q.all()]

                
class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field() 
    create_post = CreatePost.Field()
    delete_user = DeleteUser.Field()
    delete_post = DeletePost.Field()