from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.services.llm_service import LLMService

router = APIRouter()
llm_service = LLMService()

class ChatRequest(BaseModel):
    message: str

@router.post("/chat")
def chat_endpoint(req: ChatRequest):
    try:
        reply = llm_service.generate_response(req.message)
        return {"character": "Goku", "response": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
