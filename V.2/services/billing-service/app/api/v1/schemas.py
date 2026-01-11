from pydantic import BaseModel, Field
from typing import Optional


class UsageRecordRequest(BaseModel):
    user_id: str = Field(..., example="user@goku.ai")
    endpoint: str = Field(..., example="chat")
    tokens: int = Field(1, ge=1, example=1)


class UsageRecordResponse(BaseModel):
    allowed: bool
    remaining: Optional[int] = None
