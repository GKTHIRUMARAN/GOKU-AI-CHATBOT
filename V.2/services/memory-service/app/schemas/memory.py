from pydantic import BaseModel
from typing import List, Dict


class MemoryWriteRequest(BaseModel):
    user_id: str
    persona_id: str
    role: str          # user | assistant | system
    content: str
    long_term: bool = False


class MemoryContextRequest(BaseModel):
    user_id: str
    persona_id: str


class MemoryContextResponse(BaseModel):
    messages: List[Dict[str, str]]
    long_term: List[str]
