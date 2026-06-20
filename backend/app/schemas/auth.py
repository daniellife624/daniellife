from pydantic import BaseModel, EmailStr


class GoogleLoginRequest(BaseModel):
    credential: str     # Google ID token from GSI


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    name: str
    email: str


class UserOut(BaseModel):
    id: int
    name: str
    email: str

    model_config = {"from_attributes": True}
