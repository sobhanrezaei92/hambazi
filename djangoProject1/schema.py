import graphene

from Homepage.schema import Query as HomepageQuery
from Homepage.schema import Mutation as HomepageMutation


class Query(HomepageQuery, graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass


class Mutation(HomepageMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
