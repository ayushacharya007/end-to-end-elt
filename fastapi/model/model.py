"""
SQLAlchemy models for the test_dlt_dataset schema (normalized)
"""

from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Lookup/Reference Tables
class Region(Base):
    __tablename__ = 'regions'
    __table_args__ = {'schema': 'test_dlt_dataset'}
    
    region_id = Column(Integer, primary_key=True, index=True)
    region_name = Column(String, index=True)

class ReferralSource(Base):
    __tablename__ = 'referral'
    __table_args__ = {'schema': 'test_dlt_dataset'}
    
    referral_source_id = Column(Integer, primary_key=True, index=True)
    source_name = Column(String, index=True)

class PaymentMethod(Base):
    __tablename__ = 'payment_methods'
    __table_args__ = {'schema': 'test_dlt_dataset'}
    
    payment_method_id = Column(Integer, primary_key=True, index=True)
    method_name = Column(String, index=True)

class PlanFeature(Base):
    __tablename__ = 'features'
    __table_args__ = {'schema': 'test_dlt_dataset'}
    
    feature_id = Column(Integer, primary_key=True, index=True)
    plan_id = Column(Integer, ForeignKey('test_dlt_dataset.plans.plan_id'))
    feature_name = Column(String)

# Main Entity Tables (Normalized)
class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'test_dlt_dataset'}
    
    user_id = Column(String, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    signup_date = Column(String)
    plan_id = Column(Integer, ForeignKey('test_dlt_dataset.plans.plan_id'))
    region_id = Column(Integer, ForeignKey('test_dlt_dataset.regions.region_id'))
    referral_source_id = Column(Integer, ForeignKey('test_dlt_dataset.referral.referral_source_id'))
    
class Plan(Base):
    __tablename__ = 'plans'
    __table_args__ = {'schema': 'test_dlt_dataset'}
    
    plan_id = Column(Integer, primary_key=True, index=True)
    plan_name = Column(String, index=True)
    monthly_fee = Column(Float) 
    max_users = Column(String)
    api_limit = Column(Integer)
    storage_limit_mb = Column(Integer)
    project_limit = Column(String)
    
class Subscription(Base):
    __tablename__ = 'subscriptions'
    __table_args__ = {'schema': 'test_dlt_dataset'}
    
    subscription_id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey('test_dlt_dataset.users.user_id'))
    plan_id = Column(Integer, ForeignKey('test_dlt_dataset.plans.plan_id'))
    start_date = Column(String)
    end_date = Column(String)
    payment_method_id = Column(Integer, ForeignKey('test_dlt_dataset.payment_methods.payment_method_id'))
    status = Column(String, index=True)

class Usage(Base):
    __tablename__ = 'usage'
    __table_args__ = {'schema': 'test_dlt_dataset'}
    
    usage_id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey('test_dlt_dataset.users.user_id'))
    subscription_id = Column(String, ForeignKey('test_dlt_dataset.subscriptions.subscription_id'))
    usage_date = Column(String)
    actions_performed = Column(Integer)
    storage_used_mb = Column(Float)
    api_calls = Column(Integer)
    active_minutes = Column(Integer)
