from sqlalchemy.orm import Session

from app.models.billing import UserPlan, UsageRecord


def check_and_record_usage(
    db: Session,
    user_id: str,
    endpoint: str,
    tokens: int,
):
    """
    Hard-enforce monthly usage limits.
    Enterprise plan = unlimited.
    """

    plan = (
        db.query(UserPlan)
        .filter(UserPlan.user_id == user_id)
        .first()
    )

    if not plan:
        return {
            "allowed": False,
            "reason": "No active plan found",
        }

    # ✅ ENTERPRISE = UNLIMITED
    if plan.plan == "enterprise":
        record = UsageRecord(
            user_id=user_id,
            endpoint=endpoint,
            tokens=tokens,
        )
        db.add(record)
        db.commit()

        return {
            "allowed": True,
            "remaining": None,
        }

    # 🔒 Enforce monthly limit for non-enterprise
    if plan.used + tokens > plan.monthly_limit:
        return {
            "allowed": False,
            "reason": "Monthly limit exceeded",
        }

    record = UsageRecord(
        user_id=user_id,
        endpoint=endpoint,
        tokens=tokens,
    )

    plan.used += tokens

    db.add(record)
    db.add(plan)
    db.commit()

    return {
        "allowed": True,
        "remaining": plan.monthly_limit - plan.used,
    }
