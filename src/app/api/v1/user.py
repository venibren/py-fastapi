from fastapi import APIRouter, Response, status

from ...models.user import User

router = APIRouter(
    prefix="/user",
    tags=["User"],
)


@router.post(path="", status_code=status.HTTP_200_OK)
async def post_user(user: User) -> Response:
    print(
        f"Registering user: {user.first_name} {user.last_name} with email: {user.email}"
    )
    return Response(status_code=status.HTTP_200_OK)
