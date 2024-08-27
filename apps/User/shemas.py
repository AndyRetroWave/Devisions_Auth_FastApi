from pydantic import BaseModel, EmailStr


class UserShemas(BaseModel):
    id: int
    email: EmailStr
    hashed_password: str
    is_active: bool
