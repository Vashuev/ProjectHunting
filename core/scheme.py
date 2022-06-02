import graphene
from mprs.query import MprsQuery
from mprs.mutations import MprsMutation
from accounts.query import AccountQuery
from accounts.mutations import AccountMutation


class Query(AccountQuery, MprsQuery):
    pass

class Mutation(AccountMutation, MprsMutation):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)