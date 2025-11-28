from .base_schema import BaseSchema


class User(BaseSchema):
    id: int
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
