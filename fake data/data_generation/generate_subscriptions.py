"""
Generate fake subscription data
"""
import faker
from typing import List
import pandas as pd
import numpy as np
from datetime import datetime
from models import Plan, Subscription
from data_generation.generate_plans import generate_plans

def generate_subscriptions(user_df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate fake subscription data based on user data
    
    Args:
        user_df: DataFrame containing user data
        
    Returns:
        DataFrame containing subscription data
    """
    subscriptions: List[Subscription] = []
    plans = generate_plans().to_dict(orient='records')
    
    if not plans:
        raise ValueError("No plans available to generate subscriptions.")

    # Generate initial subscription for each user
    for i in range(len(user_df)):
        uid = user_df.user_id.iloc[i]
        pid = user_df.plan_id.iloc[i]
        sd = pd.to_datetime(user_df.signup_date.iloc[i])

        plan = next((plan for plan in plans if plan['plan_id'] == pid), None)
        
        if not plan:
            continue

        # Determine payment method and end date based on plan
        if plan['plan_name'] == "Free":
            pm_id = 4  # N/A
            ed = 'N/A'
            status = 'active'
        else:
            # Payment method IDs: 1=credit card, 2=paypal, 3=bank transfer
            pm_id = np.random.choice(
                [1, 2, 3],
                p=[0.60, 0.30, 0.10]
            )
            ed = sd + pd.DateOffset(months=1)

        # Determine status
        if plan['plan_name'] != "Free" and ed != 'N/A' and ed.strftime('%Y-%m-%d') < pd.to_datetime(datetime.now().date()).strftime('%Y-%m-%d'):
            st = 'expired'
        else:
            st = 'active'

        subscription = Subscription(
            subscription_id=faker.Faker().uuid4()[:8],
            user_id=uid,
            plan_id=pid,
            start_date=sd.strftime('%Y-%m-%d'),
            end_date=ed if ed == 'N/A' else ed.strftime('%Y-%m-%d'),
            payment_method_id=pm_id,
            status=st,
        )
        subscriptions.append(subscription)
    
    # Get all paid users (excluding free plan users)
    paid_user_ids = [sub.user_id for sub in subscriptions if sub.plan_id != 1]
    unique_paid_users = list(set(paid_user_ids))
    
    # Assign renewal counts to each paid user with weighted distribution
    # Most users (60%) get 7-11 renewals, some (25%) get 3-6, few (10%) get 12-20, rare (5%) get 21-30
    renewal_counts = {}
    for user_id in unique_paid_users:
        rand = np.random.random()
        if rand < 0.60:  # 60% of users: moderate renewals (7-11)
            renewal_count = np.random.randint(7, 12)
        elif rand < 0.85:  # 25% of users: fewer renewals (3-6)
            renewal_count = np.random.randint(3, 7)
        elif rand < 0.95:  # 10% of users: more renewals (12-20)
            renewal_count = np.random.randint(12, 21)
        else:  # 5% of users: heavy users (21-30)
            renewal_count = np.random.randint(21, 31)
        
        renewal_counts[user_id] = renewal_count
    
    # Generate renewals for each paid user
    for user_id, num_renewals in renewal_counts.items():
        # Get the initial subscription for this user
        user_subscriptions = [sub for sub in subscriptions if sub.user_id == user_id]
        if not user_subscriptions:
            continue
            
        last_subscription = user_subscriptions[0]
        
        # Generate multiple renewals
        for renewal_num in range(num_renewals):
            # New subscription starts 1-7 days after the previous one ended
            if last_subscription.end_date == 'N/A':
                new_start = pd.to_datetime(last_subscription.start_date) + pd.DateOffset(days=np.random.randint(30, 40))
            else:
                new_start = pd.to_datetime(last_subscription.end_date) + pd.DateOffset(days=np.random.randint(1, 8))

            # 70% chance to keep same plan, 30% chance to upgrade/downgrade
            if np.random.random() < 0.7:
                new_plan_id = last_subscription.plan_id
            else:
                # Choose a different paid plan (exclude free plan)
                available_plans = [2, 3, 4, 5]
                if last_subscription.plan_id in available_plans:
                    available_plans.remove(last_subscription.plan_id)
                new_plan_id = np.random.choice(available_plans)

            new_plan = next((plan for plan in plans if plan['plan_id'] == new_plan_id), None)
            
            if not new_plan:
                continue

            # Determine payment method and end date for new subscription
            if new_plan['plan_name'] == "Free":
                new_pm_id = 4  # N/A
                new_end = 'N/A'
                new_st = 'active'
            else:
                # Payment method IDs: 1=credit card, 2=paypal, 3=bank transfer
                new_pm_id = np.random.choice(
                    [1, 2, 3],
                    p=[0.60, 0.30, 0.10]
                )
                new_end = new_start + pd.DateOffset(months=1)

                # Determine status for new subscription
                if new_end.strftime('%Y-%m-%d') < pd.to_datetime(datetime.now().date()).strftime('%Y-%m-%d'):
                    new_st = 'expired'
                else:
                    new_st = 'active'

            new_subscription = Subscription(
                subscription_id=faker.Faker().uuid4()[:8],
                user_id=user_id,
                plan_id=new_plan_id,
                start_date=new_start.strftime('%Y-%m-%d'),
                end_date=new_end if new_end == 'N/A' else new_end.strftime('%Y-%m-%d'),
                payment_method_id=new_pm_id,
                status=new_st
            )
            subscriptions.append(new_subscription)
            
            # Update last_subscription for the next iteration
            last_subscription = new_subscription

    return pd.DataFrame([subscription.model_dump() for subscription in subscriptions])


if __name__ == "__main__":
    # Generate sample data
    from generate_users import generate_users
    
    users_df = generate_users(100)
    subscriptions_df = generate_subscriptions(users_df)
    
    print(f"Generated {len(subscriptions_df)} subscriptions for {len(users_df)} users")
    print(subscriptions_df.head())
    print(f"\nData types:\n{subscriptions_df.dtypes}")
    print(f"\nStatus distribution:\n{subscriptions_df['status'].value_counts()}")
    print(f"\n10 most renewal count:\n{subscriptions_df['user_id'].value_counts().head(10)}")