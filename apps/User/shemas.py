from pydantic import BaseModel, EmailStr


class UserShemas(BaseModel):
    id: int
    email: EmailStr
    given_name: str
    family_name: str
    hashed_password: str
    is_active: bool
