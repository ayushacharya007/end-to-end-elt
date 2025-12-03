"""
Generate fake user data
"""
import faker
from typing import List
import pandas as pd
import numpy as np
from datetime import datetime
from models import User

fake = faker.Faker(locale='en_US')


def generate_users(count: int = 1000) -> pd.DataFrame:
    """
    Generate fake user data
    
    Args:
        count: Number of users to generate
        
    Returns:
        DataFrame containing user data
    """
    users: List[User] = []
    user_id = [fake.uuid4()[:8] for _ in range(count)]
    first_name = [fake.first_name() for _ in range(count)]
    last_name = [fake.last_name() for _ in range(count)]
    email = [fake.email() for _ in range(count)]
    signup_date = [
        pd.to_datetime(
            np.random.randint(
                pd.Timestamp('2024-08-01').value,
                pd.Timestamp(datetime.now().date()).value
            )
        ).normalize().strftime('%Y-%m-%d')
        for _ in range(count)
    ]
    plan_id = [
        np.random.choice(
            [1, 2, 3, 4, 5], 
            p=[0.33, 0.27, 0.18, 0.16, 0.06]
        )
        for _ in range(count)
    ]
    # Region IDs (1-6) with equal probability
    region_id = [
        np.random.choice([1, 2, 3, 4, 5, 6])
        for _ in range(count)
    ]
    # Referral source IDs (1=web search, 2=paid ads, 3=social media, 4=referral)
    referral_source_id = [
        np.random.choice(
            [1, 2, 3, 4],
            p=[0.20, 0.45, 0.10, 0.25]
        )
        for _ in range(count)
    ]

    for i in range(count):
        user = User(
            user_id=user_id[i],
            first_name=first_name[i],
            last_name=last_name[i],
            email=email[i],
            signup_date=signup_date[i],
            plan_id=plan_id[i],
            region_id=region_id[i],
            referral_source_id=referral_source_id[i]
        )
        users.append(user)

    return pd.DataFrame([user.model_dump() for user in users])


if __name__ == "__main__":
    # Generate and display sample data
    df = generate_users(1000)
    print(f"Generated {len(df)} users")
    print(df.head())
    print(f"\nData types:\n{df.dtypes}")
