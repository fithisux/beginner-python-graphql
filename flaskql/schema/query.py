import graphene
from  flaskql.models import gqlmodel
from  flaskql.models import dao
from flaskql import db


class Query(graphene.ObjectType):
    user = graphene.Field(gqlmodel.GQLUser, username = graphene.String())
    post = graphene.Field(gqlmodel.GQLPost, title = graphene.String())
    allusers = graphene.List(gqlmodel.GQLUser) 
    allposts = graphene.List(gqlmodel.GQLPost) 
    
    def resolve_user(self, info,  username=None):
        result = None
        
        with(db.grab_session(db.get_db())) as session:
            q = session.query(dao.User)
            result = gqlmodel.GQLUser.convert(q.filter(dao.User.username == username).one())
        
        return result

    def resolve_post(self, info, title=None): 
        result = None
           
        with(db.grab_session(db.get_db())) as session:
            q = session.query(dao.Post)
            result = gqlmodel.GQLPost.convert(q.filter(dao.Post.title == title).one())
        
        return result
    
    def resolve_allusers(self, info):
        result = None
        
        with(db.grab_session(db.get_db())) as session:
            q = session.query(dao.User)
            result = [gqlmodel.GQLUser.convert(user) for user in q.all()]
        
        return result

    def resolve_allposts(self, info):   
        result = None
         
        with(db.grab_session(db.get_db())) as session:
            q = session.query(dao.Post)
            result = [gqlmodel.GQLPost.convert(post) for post in q.all()]
        
        return result
