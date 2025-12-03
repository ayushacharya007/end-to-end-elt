"""
Pydantic models for fake data generation
"""
from pydantic import BaseModel, EmailStr
from typing import List
class User(BaseModel):
    user_id: str
    first_name: str
    last_name: str
    email: EmailStr
    signup_date: str
    plan_id: int
    region: str
    referral_source: str


class Plan(BaseModel):
    plan_id: int
    plan_name: str
    monthly_fee: float
    max_users: int | str
    api_limit: int
    storage_limit_mb: int
    project_limit: int | str
    features: List[str]


class Subscription(BaseModel):
    subscription_id: str
    user_id: str
    plan_id: int
    start_date: str
    end_date: str
    payment_method: str
    status: str


class Usage(BaseModel):
    usage_id: str
    user_id: str
    usage_date: str
    actions_performed: int
    storage_used_mb: float
    api_calls: int
    active_minutes: int
    plan_id: int
