from sqlalchemy import Column, Integer, String, DateTime, func
from app.db.base import Base


class UserPlan(Base):
    __tablename__ = "user_plans"

    id = Column(Integer, primary_key=True)
    user_id = Column(String(255), unique=True, nullable=False)

    # MUST match DB column
    plan = Column(String(50), nullable=False)

    monthly_limit = Column(Integer, nullable=False)
    used = Column(Integer, nullable=False, default=0)


class UsageRecord(Base):
    __tablename__ = "usage_records"

    id = Column(Integer, primary_key=True)
    user_id = Column(String(255), nullable=False)
    endpoint = Column(String(100), nullable=False)
    tokens = Column(Integer, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
