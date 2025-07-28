from pydantic import BaseModel, ConfigDict

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

class User(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
