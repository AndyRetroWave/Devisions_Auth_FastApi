from fastapi import APIRouter

router = APIRouter(
    prefix="/auth",
    tags=["Auth & Пользователи"]
)


@router.get('/')
def get_auth():
    return {"auth": "ok"}
