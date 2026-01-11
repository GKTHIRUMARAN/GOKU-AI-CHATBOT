from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.v1.schemas import UsageRecordRequest, UsageRecordResponse
from app.db.session import SessionLocal
from app.services.usage_service import check_and_record_usage

router = APIRouter(prefix="/usage", tags=["Usage"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/record", response_model=UsageRecordResponse)
def record_usage(
    payload: UsageRecordRequest,
    db: Session = Depends(get_db),
):
    result = check_and_record_usage(
        db=db,
        user_id=payload.user_id,
        endpoint=payload.endpoint,
        tokens=payload.tokens,
    )

    if not result["allowed"]:
        raise HTTPException(
            status_code=429,
            detail=result["reason"],
        )

    return UsageRecordResponse(
        allowed=True,
        remaining=result.get("remaining"),
    )
