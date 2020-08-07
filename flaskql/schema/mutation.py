import datetime
import graphene
from  flaskql.models import gqlmodel
from  flaskql.models import dao
from flaskql import db

class CreateUser(graphene.Mutation):
    class Arguments:
        username = graphene.String()
        password = graphene.String()
                
    ok = graphene.Boolean()
    user = graphene.Field(gqlmodel.GQLUser)
 
    def mutate(self, info, username=None, password = None):
        result = None
        
        with(db.grab_session()) as session:
            user = dao.User(username=username, password=password)
            session.add(user)
            session.commit()
            ok = True
            result = CreateUser(user=gqlmodel.GQLUser.convert(user), ok=ok)
        
        return result
     
class CreatePost(graphene.Mutation):
    class Arguments:
        userId = graphene.Int()
        title = graphene.String()
        body = graphene.String()
        
    ok = graphene.Boolean()
    post = graphene.Field(gqlmodel.GQLPost)
 
    def mutate(self, info, userId=None, title=None, body=None):
        result = None
        
        with(db.grab_session()) as session:
            user = session.query(dao.User).filter(dao.User.id == userId).one()
        
            if user == None:
                ok = False
                post = None
            else:
                post = dao.Post(title = title, body = body , created = datetime.datetime.now(), user = user)
                session.add(post)
                session.commit()
                ok = True
                
            result = CreatePost(post=gqlmodel.GQLPost.convert(post), ok=ok)
        
        return result
     
class DeleteUser(graphene.Mutation):
    class Arguments:
        userId = graphene.Int()
        
    ok = graphene.Boolean()
    user = graphene.Field(gqlmodel.GQLUser)
 
    def mutate(self, info, userId=None):
        result = None
        
        with(db.grab_session()) as session:
            q = session.query(dao.User).filter(dao.User.id == userId)
            user = q.one()
        
            if user == None:
                ok = False
            else:
                q.delete()
                session.commit()
                ok = True
                
            result = DeleteUser(user=gqlmodel.GQLUser.convert(user), ok=ok)
        
        return result
     
class DeletePost(graphene.Mutation):
    class Arguments:
        postId = graphene.Int()
        
    ok = graphene.Boolean()
    post = graphene.Field(gqlmodel.GQLPost)
 
    def mutate(self, info, postId=None):
        result = None
        
        with(db.grab_session()) as session:
            q = session.query(dao.Post).filter(dao.Post.id == postId)
            post = q.one()
        
            if post == None:
                ok = False
            else:
                q.delete()
                session.commit()
                ok = True
                
            result = DeletePost(post=gqlmodel.GQLPost.convert(post), ok=ok)    
        
        return result
                
class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field() 
    create_post = CreatePost.Field()
    delete_user = DeleteUser.Field()
    delete_post = DeletePost.Field()