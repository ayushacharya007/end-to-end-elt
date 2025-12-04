"""
Generate fake usage data with quota tracking and limits enforcement
"""
import faker
from typing import List, Dict
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from models import Usage
from data_generation.generate_plans import generate_plans

fake = faker.Faker(locale='en_US')


def generate_usage(user_df: pd.DataFrame, subscription_df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate realistic usage data with quota enforcement
    
    Key Features:
    - Tracks cumulative usage per subscription period
    - Enforces plan limits (API calls, storage)
    - Users who hit limits stop generating usage until next renewal
    - Realistic quota exhaustion patterns (some users hit limits, most don't)
    
    Args:
        user_df: DataFrame containing user data
        subscription_df: DataFrame containing subscription data
        
    Returns:
        DataFrame containing usage data with quota enforcement
    """
    usages: List[Usage] = []
    
    # Load plan limits
    plans_df = generate_plans()
    plan_limits = {
        row['plan_id']: {
            'api_limit': row['api_limit'],
            'storage_limit_mb': row['storage_limit_mb']
        }
        for _, row in plans_df.iterrows()
    }
    
    # Assign engagement level to each user (affects usage frequency and quota exhaustion)
    user_engagement = {}
    for user_id in user_df.user_id.unique():
        rand = np.random.random()
        if rand < 0.15:  # 15% heavy users (daily usage, likely to hit limits)
            engagement = 'heavy'
        elif rand < 0.55:  # 40% moderate users (3-5 times per week)
            engagement = 'moderate'
        else:  # 45% light users (1-2 times per week, rarely hit limits)
            engagement = 'light'
        user_engagement[user_id] = engagement
    
    # Generate usage for EACH subscription with quota tracking
    for _, sub in subscription_df.iterrows():
        user_id = sub['user_id']
        plan_id = sub['plan_id']
        subscription_id = sub['subscription_id']
        
        # Get plan limits
        limits = plan_limits.get(plan_id, None)
        if limits is None:
            continue
        monthly_api_limit = limits['api_limit']
        monthly_storage_limit = limits['storage_limit_mb']
        
        # Track cumulative usage for this subscription period
        cumulative_api_calls = 0
        cumulative_storage_mb = 0.0
        quota_exhausted = False
        
        # Skip free users - they might have minimal usage
        if plan_id == 1:
            usage_probability = 0.3  # 30% chance of usage on any given day
        else:
            usage_probability = 1.0  # Paid users have regular usage
        
        start_date = pd.to_datetime(sub['start_date'])
        end_date = pd.to_datetime(sub['end_date']) if sub['end_date'] != 'N/A' else pd.to_datetime(datetime.now().date())
        
        # Ensure valid date range
        if start_date >= end_date:
            end_date = start_date + pd.DateOffset(days=1)
        
        # Determine usage frequency based on engagement level
        engagement = user_engagement.get(user_id, 'moderate')
        if engagement == 'heavy':
            days_between_usage = 1  # Daily
            # Heavy users have higher chance of hitting quota
            quota_hit_probability = 0.4 if plan_id in [1, 2] else 0.15
        elif engagement == 'moderate':
            days_between_usage = 2  # Every 2-3 days
            quota_hit_probability = 0.15 if plan_id in [1, 2] else 0.05
        else:
            days_between_usage = 4  # Every 4-7 days
            quota_hit_probability = 0.05 if plan_id in [1, 2] else 0.01
        
        # Determine if this user will hit quota this month
        will_hit_quota = np.random.random() < quota_hit_probability
        
        # Generate usage records for this subscription period
        current_date = start_date
        usage_count = 0
        max_usage_per_subscription = 60  # Cap to avoid too many records
        
        while current_date <= end_date and usage_count < max_usage_per_subscription and not quota_exhausted:
            # Add some randomness to usage frequency
            days_to_add = days_between_usage + np.random.randint(-1, 3)
            days_to_add = max(1, days_to_add)  # At least 1 day
            
            current_date += pd.DateOffset(days=days_to_add)
            
            if current_date > end_date:
                break
            
            # Skip some days randomly based on usage probability
            if np.random.random() > usage_probability:
                continue
            
            # Weekday vs Weekend pattern (lower usage on weekends)
            is_weekend = current_date.weekday() >= 5
            weekend_factor = 0.6 if is_weekend else 1.0
            
            # Growth pattern: usage tends to increase over time within a subscription
            days_into_subscription = (current_date - start_date).days
            total_subscription_days = (end_date - start_date).days
            growth_factor = 1.0 + (days_into_subscription / max(total_subscription_days, 1)) * 0.3
            
            # If user will hit quota, make them use more resources as they approach the limit
            if will_hit_quota:
                # Aggressive usage multiplier (1.5x to 2.5x normal)
                aggressive_factor = np.random.uniform(1.5, 2.5)
            else:
                # Normal usage (0.5x to 1.2x)
                aggressive_factor = np.random.uniform(0.5, 1.2)
            
            # Generate correlated metrics based on plan
            base_multiplier = weekend_factor * growth_factor * aggressive_factor
            
            # Plan-based usage patterns with beta distribution
            # Adjusted to align with new realistic plan limits
            if plan_id == 1:  # Free (100 API/month, 500 MB storage)
                storage_increment = round((5 + np.random.beta(2, 5) * 45) * base_multiplier, 2)  # 5-50 MB per use
                api = int((1 + np.random.beta(2, 5) * 9) * base_multiplier)  # 1-10 API calls per use
                actions = int((3 + np.random.beta(2, 5) * 17) * base_multiplier)  # 3-20 actions
                active_mins = int((5 + np.random.beta(2, 5) * 55) * base_multiplier)  # 5-60 mins
            elif plan_id == 2:  # Starter (1,000 API/month, 5 GB storage)
                storage_increment = round((50 + np.random.beta(2, 5) * 450) * base_multiplier, 2)  # 50-500 MB per use
                api = int((10 + np.random.beta(2, 5) * 90) * base_multiplier)  # 10-100 API calls per use
                actions = int((10 + np.random.beta(2, 5) * 90) * base_multiplier)  # 10-100 actions
                active_mins = int((15 + np.random.beta(2, 5) * 135) * base_multiplier)  # 15-150 mins
            elif plan_id == 3:  # Professional (10,000 API/month, 50 GB storage)
                storage_increment = round((500 + np.random.beta(2, 5) * 4500) * base_multiplier, 2)  # 500-5000 MB per use
                api = int((100 + np.random.beta(2, 5) * 900) * base_multiplier)  # 100-1000 API calls per use
                actions = int((50 + np.random.beta(2, 5) * 450) * base_multiplier)  # 50-500 actions
                active_mins = int((30 + np.random.beta(2, 5) * 270) * base_multiplier)  # 30-300 mins
            elif plan_id == 4:  # Business (50,000 API/month, 200 GB storage)
                storage_increment = round((2000 + np.random.beta(2, 5) * 18000) * base_multiplier, 2)  # 2-20 GB per use
                api = int((500 + np.random.beta(2, 5) * 4500) * base_multiplier)  # 500-5000 API calls per use
                actions = int((100 + np.random.beta(2, 5) * 900) * base_multiplier)  # 100-1000 actions
                active_mins = int((60 + np.random.beta(2, 5) * 540) * base_multiplier)  # 60-600 mins
            else:  # Enterprise (250,000 API/month, 1 TB storage)
                storage_increment = round((10000 + np.random.beta(2, 5) * 90000) * base_multiplier, 2)  # 10-100 GB per use
                api = int((2500 + np.random.beta(2, 5) * 22500) * base_multiplier)  # 2500-25000 API calls per use
                actions = int((500 + np.random.beta(2, 5) * 4500) * base_multiplier)  # 500-5000 actions
                active_mins = int((120 + np.random.beta(2, 5) * 1080) * base_multiplier)  # 120-1200 mins
            
            # Add correlation noise: higher API calls should correlate with more actions
            correlation_factor = np.random.uniform(0.8, 1.2)
            actions = int(actions * correlation_factor)
            
            # CHECK QUOTA LIMITS BEFORE ADDING USAGE
            # Check if adding this usage would exceed limits
            potential_api_total = cumulative_api_calls + api
            potential_storage_total = cumulative_storage_mb + storage_increment
            
            # API Limit Check
            if potential_api_total > monthly_api_limit:
                # User hit API limit - cap at limit and mark quota exhausted
                api = max(0, monthly_api_limit - cumulative_api_calls)
                quota_exhausted = True
            
            # Storage Limit Check
            if potential_storage_total > monthly_storage_limit:
                # User hit storage limit - cap at limit and mark quota exhausted
                storage_increment = max(0, monthly_storage_limit - cumulative_storage_mb)
                quota_exhausted = True
            
            # Update cumulative usage
            cumulative_api_calls += api
            cumulative_storage_mb += storage_increment
            
            # Only create usage record if there's actual usage
            if api > 0 or storage_increment > 0:
                usage = Usage(
                    usage_id=fake.uuid4()[:8],
                    user_id=user_id,
                    subscription_id=subscription_id,
                    usage_date=current_date.strftime('%Y-%m-%d'),
                    actions_performed=max(1, actions),
                    storage_used_mb=max(0.1, storage_increment),
                    api_calls=max(1, api),
                    active_minutes=max(1, active_mins)
                )
                usages.append(usage)
                usage_count += 1
            
            # If quota exhausted, stop generating usage for this subscription period
            if quota_exhausted:
                break
    
    return pd.DataFrame([usage.model_dump() for usage in usages])


if __name__ == "__main__":
    # Generate sample data
    from generate_users import generate_users
    from generate_subscriptions import generate_subscriptions
    
    print("Generating users...")
    users_df = generate_users(1000)
    
    print("Generating subscriptions...")
    subscriptions_df = generate_subscriptions(users_df)
    
    print("Generating usage data with quota enforcement...")
    usage_df = generate_usage_with_quotas(users_df, subscriptions_df)
    
    print(f"\n{'='*70}")
    print(f"Generated {len(usage_df)} usage records for {len(users_df)} users")
    print(f"Across {len(subscriptions_df)} subscriptions")
    print(f"{'='*70}\n")
    
    print("Sample usage records:")
    print(usage_df.head(10))
    
    print(f"\n{'='*70}")
    print("Usage statistics by metric:")
    print(usage_df[['actions_performed', 'storage_used_mb', 'api_calls', 'active_minutes']].describe())
    
    print(f"\n{'='*70}")
    print("Usage distribution by plan:")
    plan_stats = usage_df.groupby('plan_id').agg({
        'usage_id': 'count',
        'actions_performed': 'mean',
        'storage_used_mb': ['mean', 'sum'],
        'api_calls': ['mean', 'sum'],
        'active_minutes': 'mean'
    }).round(2)
    print(plan_stats)
    
    print(f"\n{'='*70}")
    print("Quota Analysis - Checking for users who hit limits:")
    
    # Load plan limits for comparison
    plans_df = generate_plans()
    
    # Analyze quota usage per subscription
    quota_analysis = []
    for _, sub in subscriptions_df.iterrows():
        sub_usage = usage_df[usage_df['user_id'] == sub['user_id']]
        
        # Filter usage for this specific subscription period
        start_date = pd.to_datetime(sub['start_date'])
        end_date = pd.to_datetime(sub['end_date']) if sub['end_date'] != 'N/A' else pd.to_datetime(datetime.now().date())
        
        sub_usage_filtered = sub_usage[
            (pd.to_datetime(sub_usage['usage_date']) >= start_date) &
            (pd.to_datetime(sub_usage['usage_date']) <= end_date)
        ]
        
        if len(sub_usage_filtered) > 0:
            total_api = sub_usage_filtered['api_calls'].sum()
            total_storage = sub_usage_filtered['storage_used_mb'].sum()
            
            plan_info = plans_df[plans_df['plan_id'] == sub['plan_id']].iloc[0]
            api_limit = plan_info['api_limit']
            storage_limit = plan_info['storage_limit_mb']
            
            api_usage_pct = (total_api / api_limit) * 100
            storage_usage_pct = (total_storage / storage_limit) * 100
            
            quota_analysis.append({
                'user_id': sub['user_id'],
                'plan_id': sub['plan_id'],
                'plan_name': plan_info['plan_name'],
                'api_used': total_api,
                'api_limit': api_limit,
                'api_usage_pct': round(api_usage_pct, 1),
                'storage_used': round(total_storage, 2),
                'storage_limit': storage_limit,
                'storage_usage_pct': round(storage_usage_pct, 1),
                'hit_limit': api_usage_pct >= 99 or storage_usage_pct >= 99
            })
    
    quota_df = pd.DataFrame(quota_analysis)
    
    print(f"\nUsers who hit their quota limits (>99% usage):")
    limit_hitters = quota_df[quota_df['hit_limit'] == True]
    if len(limit_hitters) > 0:
        print(limit_hitters[['user_id', 'plan_name', 'api_usage_pct', 'storage_usage_pct']].tail(10))
    else:
        print("No users hit their limits in this dataset")
    
    print(f"\n{'='*70}")
    print("Quota usage distribution:")
    print(f"Users at 90-100% quota: {len(quota_df[quota_df['api_usage_pct'] >= 90])}")
    print(f"Users at 70-90% quota: {len(quota_df[(quota_df['api_usage_pct'] >= 70) & (quota_df['api_usage_pct'] < 90)])}")
    print(f"Users at 50-70% quota: {len(quota_df[(quota_df['api_usage_pct'] >= 50) & (quota_df['api_usage_pct'] < 70)])}")
    print(f"Users below 50% quota: {len(quota_df[quota_df['api_usage_pct'] < 50])}")
