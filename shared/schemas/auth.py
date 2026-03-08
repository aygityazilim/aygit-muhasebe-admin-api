from pydantic import BaseModel, Field

class LoginSchema(BaseModel):
    email: str = Field(...)
    password: str = Field(...)