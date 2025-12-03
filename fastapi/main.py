"""
Script to create FastAPI application with basic authentication and database access
Run this to start the FastAPI server
"""

from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination import Page, add_pagination
from config.config import session, engine
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Annotated
from model import model
from model.schema import User, Subscription, Usage
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="../.env")  # provide correct path to your .env file

app = FastAPI()
add_pagination(app)

# Only create tables when explicitly enabled (e.g., local dev)
if os.getenv("RUN_CREATE_ALL", "false").lower() == "true":
    model.Base.metadata.create_all(bind=engine)

security = HTTPBasic()

username = os.environ["BASIC_AUTH_USERNAME"]
password = os.environ["BASIC_AUTH_PASSWORD"]

if username is None or password is None:
    raise ValueError("BASIC_AUTH_USERNAME and BASIC_AUTH_PASSWORD environment variables must be set")

# Helper function to verify credentials from query parameters
def verify_credentials(
    username_param: str = Query(..., alias="username", description="Username for authentication"),
    password_param: str = Query(..., alias="password", description="Password for authentication")
):
    # Direct string comparison - simple and secure for environment-based credentials
    if username_param == username and password_param == password:
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials"
    )

@app.get("/")
def home(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    if credentials.username == username and credentials.password == password:
        return {"message": "Welcome to the FastAPI application!"}
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unauthorized",
        headers={"WWW-Authenticate": "Basic"},
    )
    

def get_db():
    # Dummy database session generator
    db = session()
    try:
        yield db
    finally:
        db.close()

@app.get("/check-tables")
def check_tables(db: Session = Depends(get_db)):
    try:
        # Check what tables exist in test_dlt schema
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names(schema='test_dlt_dataset')
        return {"Table List": tables}
    except Exception as e:
        import traceback
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": str(e), "traceback": traceback.format_exc()}
        )

# Lookup Table Endpoints
@app.get("/regions")
def get_regions(auth = Depends(verify_credentials), db: Session = Depends(get_db)):
    try:        
        regions = db.query(model.Region).all()
        if len(regions) == 0:
            return {"message": "No regions found."}
        else:
            return {"data": regions}
    except Exception as e:
        import traceback
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": str(e), "traceback": traceback.format_exc()}
        )

@app.get("/referral-sources")
def get_referral_sources(auth = Depends(verify_credentials), db: Session = Depends(get_db)):
    try:        
        sources = db.query(model.ReferralSource).all()
        if len(sources) == 0:
            return {"message": "No referral sources found."}
        else:
            return {"data": sources}
    except Exception as e:
        import traceback
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": str(e), "traceback": traceback.format_exc()}
        )

@app.get("/payment-methods")
def get_payment_methods(auth = Depends(verify_credentials), db: Session = Depends(get_db)):
    try:        
        methods = db.query(model.PaymentMethod).all()
        if len(methods) == 0:
            return {"message": "No payment methods found."}
        else:
            return {"data": methods}
    except Exception as e:
        import traceback
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": str(e), "traceback": traceback.format_exc()}
        )
@app.get("/plan-features")
def get_plan_features(auth = Depends(verify_credentials), db: Session = Depends(get_db)):
    try:        
        features = db.query(model.PlanFeature).all()
        if len(features) == 0:
            return {"message": "No plan features found."}
        else:
            return {"data": features}
    except Exception as e:
        import traceback
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": str(e), "traceback": traceback.format_exc()}
        )

# Main Entity Endpoints
@app.get("/users", response_model=Page[User])
def get_users(auth = Depends(verify_credentials), db: Session = Depends(get_db)):
    try:
        return paginate(db, select(model.User))
    except Exception as e:
        import traceback
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": str(e), "traceback": traceback.format_exc()}
        )
        
@app.get("/plans")
def get_plans(auth = Depends(verify_credentials), db: Session = Depends(get_db)):
    try:
        plans = db.query(model.Plan).all()
        if len(plans) == 0:
            return {"message": "No plans found."}
        else:
            return {"data": plans}
    except Exception as e:
        import traceback
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": str(e), "traceback": traceback.format_exc()}
        )
    
@app.get("/subscriptions", response_model=Page[Subscription])
def get_subscriptions(auth = Depends(verify_credentials), db: Session = Depends(get_db)):
    try:
        return paginate(db, select(model.Subscription))
    except Exception as e:
        import traceback
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": str(e), "traceback": traceback.format_exc()}
        )
    

@app.get("/usages", response_model=Page[Usage])
def get_usages(auth = Depends(verify_credentials), db: Session = Depends(get_db)):
    try:
        return paginate(db, select(model.Usage))
    except Exception as e:
        import traceback
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": str(e), "traceback": traceback.format_exc()}
        )