import graphene
from flaskql.models import dao


class GQLUser(graphene.ObjectType):
    username = graphene.String()
    password = graphene.String()
    id = graphene.Int()
    
    @staticmethod
    def convert(user : dao.User):
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
    def convert(post : dao.Post):
        if post == None :
            return None
        else:
            gqlPost = GQLPost()
            gqlPost.body = post.body
            gqlPost.title = post.title
            gqlPost.id = post.id
            gqlPost.created = post.created
            gqlPost.user = GQLUser.convert(post.user)
            return gqlPost