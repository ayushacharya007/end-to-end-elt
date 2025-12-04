"""
Pydantic models defining the schema for various entities in the FastAPI application.
"""
from pydantic import BaseModel, EmailStr

# Main Entity Models (Normalized)
class User(BaseModel):
    user_id: str
    first_name: str
    last_name: str
    email: EmailStr
    signup_date: str
    plan_id: int
    region_id: int  # FK to regions
    referral_source_id: int  # FK to referral_sources

class Subscription(BaseModel):
    subscription_id: str
    user_id: str
    plan_id: int
    start_date: str
    end_date: str
    payment_method_id: int  # FK to payment_methods
    status: str


class Usage(BaseModel):
    usage_id: str
    user_id: str
    subscription_id: str  # FK to subscriptions
    usage_date: str
    actions_performed: int
    storage_used_mb: float
    api_calls: int
    active_minutes: int
