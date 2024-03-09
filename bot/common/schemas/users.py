from pydantic import BaseModel, Field


class User(BaseModel):
    user_id: int = Field(..., description="User identifier")
    language_code: str = Field(..., description="Language code")
