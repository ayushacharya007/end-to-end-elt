from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from config import session, engine
from sqlalchemy.orm import Session
from typing import Annotated
import model
import os

app = FastAPI()

model.Base.metadata.create_all(bind=engine)

security = HTTPBasic()

username = os.getenv("BASIC_AUTH_USERNAME")
password = os.getenv("BASIC_AUTH_PASSWORD")

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
        # Check what tables exist in faker_dlt_dataset schema
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names(schema='faker_dlt_dataset')
        return {"Table List": tables}
    except Exception as e:
        import traceback
        return {"error": str(e), "traceback": traceback.format_exc()}

@app.get("/users")
def get_users(auth = Depends(verify_credentials),db: Session = Depends(get_db)):
    try:        
        users = db.query(model.User).all()
        if len(users) == 0:
            return {"message": "No users found."}
        else:
            return {"users": users}
    except Exception as e:
        import traceback
        return {"error": str(e), "traceback": traceback.format_exc()}

@app.get("/plans")
def get_plans(auth = Depends(verify_credentials),db: Session = Depends(get_db)):
    try:        
        plans = db.query(model.Plan).all()
        if len(plans) == 0:
            return {"message": "No plans found."}
        else:
            return {"plans": plans}
    except Exception as e:
        import traceback
        return {"error": str(e), "traceback": traceback.format_exc()}
    
@app.get("/subscriptions")
def get_subscriptions(auth = Depends(verify_credentials), db: Session = Depends(get_db)):
    try:        
        subscriptions = db.query(model.Subscription).all()
        if len(subscriptions) == 0:
            return {"message": "No subscriptions found."}
        else:
            return {"subscriptions": subscriptions}
    except Exception as e:
        import traceback
        return {"error": str(e), "traceback": traceback.format_exc()}
    

@app.get("/usages")
def get_usages(auth = Depends(verify_credentials), db: Session = Depends(get_db)):
    try:        
        usages = db.query(model.Usage).all()
        if len(usages) == 0:
            return {"message": "No usages found."}
        else:
            return {"usages": usages}
    except Exception as e:
        import traceback
        return {"error": str(e), "traceback": traceback.format_exc()}
    