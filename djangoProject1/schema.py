import graphene

from Homepage.schema import Query as HomepageQuery


class Query(HomepageQuery, graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass


schema = graphene.Schema(query=Query)
