import strawberry
from fastapi import APIRouter
from strawberry.fastapi import GraphQLRouter
from typing import Annotated
from uuid import UUID


@strawberry.type
class User:
    id: UUID
    username: str
    email: str


@strawberry.type
class Query:
    @strawberry.field
    def get_user(
        self,
        id: Annotated[UUID, strawberry.argument(description="The UUID of the user")],
    ) -> User:
        # Example implementation; replace with your data access
        return User(id=id, username="testuser", email="")


schema = strawberry.Schema(query=Query)
graphql_app = GraphQLRouter(schema, path="/graphql")

#
router = APIRouter(prefix="", tags=["GraphQL"])
router.include_router(graphql_app)
