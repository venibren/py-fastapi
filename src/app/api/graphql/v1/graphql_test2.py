from typing import Annotated
from uuid import UUID

import strawberry
from fastapi import APIRouter
from strawberry.fastapi import GraphQLRouter


@strawberry.type
class Item:
    id: UUID
    title: str
    description: str


@strawberry.type
class Query:
    @strawberry.field
    def get_item(
        self,
        id: Annotated[UUID, strawberry.argument(description="The UUID of the item")],
    ) -> Item:
        # Testing
        return Item(
            id=id, title="Book", description="A random book you find on a shelf."
        )


# Create schema and GraphQL router
schema = strawberry.Schema(query=Query)

# graphql_app = GraphQLRouter(schema, path="/graphql")

# Attach the GraphQL router to the FastAPI router
# router = APIRouter(prefix="", tags=["GraphQL"])
# router.include_router(graphql_app)
