"""
Generate plan data
"""
from typing import List
import pandas as pd
from models import Plan


def generate_plans() -> pd.DataFrame:
    """
    Generate plan data (static data)
    
    Returns:
        DataFrame containing plan data
    """
    plans = [
        Plan(
            plan_id=1,
            plan_name='Free',
            monthly_fee=0.0,
            max_users='2',
            api_limit=100,
            storage_limit_mb=500,
            project_limit=3
        ),
        Plan(
            plan_id=2,
            plan_name='Starter',
            monthly_fee=15.0,
            max_users='5',
            api_limit=1000,
            storage_limit_mb=5000,
            project_limit=10
        ),
        Plan(
            plan_id=3,
            plan_name='Professional',
            monthly_fee=49.0,
            max_users='20',
            api_limit=10000,
            storage_limit_mb=50000,
            project_limit=50
        ),
        Plan(
            plan_id=4,
            plan_name='Business',
            monthly_fee=99.0,
            max_users='100',
            api_limit=50000,
            storage_limit_mb=200000,
            project_limit=200
        ),
        Plan(
            plan_id=5,
            plan_name='Enterprise',
            monthly_fee=299.0,
            max_users='unlimited',
            api_limit=250000,
            storage_limit_mb=1000000,
            project_limit='unlimited'
        )
    ]

    return pd.DataFrame([plan.model_dump() for plan in plans])


if __name__ == "__main__":
    # Generate and display plan data
    df = generate_plans()
    print(f"Generated {len(df)} plans")
    print(df)
    print(f"\nData types:\n{df.dtypes}")
