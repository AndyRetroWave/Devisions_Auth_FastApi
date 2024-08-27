from fastapi import APIRouter

router = APIRouter(
    prefix="/auth",
    tags=["Auth & Пользователи"]
)


@router.get('/login')
async def get_auth():
    return {"auth": "ok"}
