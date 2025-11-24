from typing import Annotated
from uuid import UUID

import strawberry
from fastapi import APIRouter
from strawberry.fastapi import GraphQLRouter


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
        # Testing
        return User(id=id, username="testuser", email="")


# Create schema and GraphQL router
schema = strawberry.Schema(query=Query)
# graphql_app = GraphQLRouter(schema, path="/graphql")

# Attach the GraphQL router to the FastAPI router
# router = APIRouter(prefix="", tags=["GraphQL"])
# router.include_router(graphql_app)
