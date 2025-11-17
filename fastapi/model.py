"""
SQLAlchemy models for the faker_dlt_dataset schema
"""

from sqlalchemy import Column, Integer, String, Float, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    __table_args__ = {'schema': 'faker_dlt_dataset'}
    
    user_id = Column(String, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    signup_date = Column(String)
    plan_id = Column(Integer)
    region = Column(String)
    referral_source = Column(String)
    
class Plan(Base):
    __tablename__ = 'plan'
    __table_args__ = {'schema': 'faker_dlt_dataset'}
    
    plan_id = Column(Integer, primary_key=True, index=True)
    plan_name = Column(String, index=True)
    monthly_fee = Column(Float) 
    max_users = Column(String)
    features = Column(JSON)
    
class Subscription(Base):
    __tablename__ = 'subscription'
    __table_args__ = {'schema': 'faker_dlt_dataset'}
    
    subscription_id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey('faker_dlt_dataset.user.user_id'))
    plan_id = Column(Integer, ForeignKey('faker_dlt_dataset.plan.plan_id'))
    start_date = Column(String)
    end_date = Column(String)
    payment_method = Column(String)
    status = Column(String, index=True)

class Usage(Base):
    __tablename__ = 'usage'
    __table_args__ = {'schema': 'faker_dlt_dataset'}
    
    usage_id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey('faker_dlt_dataset.user.user_id'))
    plan_id = Column(Integer, ForeignKey('faker_dlt_dataset.plan.plan_id'))
    usage_date = Column(String)
    actions_performed = Column(Integer)
    storage_used_mb = Column(Float)
    api_calls = Column(Integer)
    active_minutes = Column(Integer)
