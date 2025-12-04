"""
Pydantic models for fake data generation
"""
from pydantic import BaseModel, EmailStr
from typing import List


# Lookup/Reference Table Models
class Region(BaseModel):
    region_id: int
    region_name: str


class ReferralSource(BaseModel):
    referral_source_id: int
    source_name: str


class PaymentMethod(BaseModel):
    payment_method_id: int
    method_name: str


class PlanFeature(BaseModel):
    feature_id: int
    plan_id: int
    feature_name: str


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


class Plan(BaseModel):
    plan_id: int
    plan_name: str
    monthly_fee: float
    max_users: int | str
    api_limit: int
    storage_limit_mb: int
    project_limit: int | str


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
