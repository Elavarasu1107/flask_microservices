from pydantic import BaseModel, EmailStr, Field, StrictInt


class RegisterSchema(BaseModel):
    username: str = Field(min_length=1)
    password: str = Field(min_length=8)
    first_name: str = None
    last_name: str = None
    email: EmailStr
    phone: StrictInt = None
    location: str = None


class LoginSchema(BaseModel):
    username: str = Field(min_length=1)
    password: str = Field(min_length=8)
