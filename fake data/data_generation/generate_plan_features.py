"""
Generate plan features bridge table
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
from models import PlanFeature
from data_generation.generate_plans import generate_plans


def generate_plan_features() -> pd.DataFrame:
    """
    Generate plan features (normalized from Plan.features array)
    
    Returns:
        DataFrame with feature_id, plan_id, feature_name
    """
    # Define features for each plan (matching the original plan definitions)
    plan_features_data = [
        # Free plan (plan_id=1)
        (1, "community support"),
        (1, "basic dashboard"),
        (1, "email notifications"), 
        (1, "7-day data retention"),
        
        # Starter plan (plan_id=2)
        (2, "email support (48h response)"),
        (2, "advanced dashboard"),
        (2, "Slack integration"),
        (2, "30-day data retention"),
        (2, "export to CSV/Excel"),
        
        # Professional plan (plan_id=3)
        (3, "priority email support (24h response)"),
        (3, "custom dashboards"),
        (3, "Slack + Google Drive + Dropbox integration"),
        (3, "90-day data retention"),
        (3, "API access"),
        (3, "webhooks"),
        (3, "2FA authentication"),
        (3, "team collaboration tools"),
        
        # Business plan (plan_id=4)
        (4, "24/7 chat + email support"),
        (4, "dedicated account manager"),
        (4, "all integrations (Zapier, Jira, Salesforce, etc.)"),
        (4, "1-year data retention"),
        (4, "advanced API access"),
        (4, "custom webhooks"),
        (4, "SSO (SAML/OAuth)"),
        (4, "role-based access control (RBAC)"),
        (4, "audit logs"),
        (4, "99.9% uptime SLA"),
        (4, "white-label reports"),
        
        # Enterprise plan (plan_id=5)
        (5, "24/7 phone + chat + email support"),
        (5, "dedicated success engineer"),
        (5, "custom integrations"),
        (5, "unlimited data retention"),
        (5, "unlimited API access"),
        (5, "custom webhooks + event streaming"),
        (5, "advanced SSO (SAML/OAuth/LDAP)"),
        (5, "advanced RBAC + permissions"),
        (5, "real-time audit logs"),
        (5, "99.99% uptime SLA"),
        (5, "custom SLA available"),
        (5, "white-label platform"),
        (5, "on-premise deployment option"),
        (5, "AI-powered analytics"),
        (5, "custom training sessions"),
    ]
    
    features = []
    for feature_id, (plan_id, feature_name) in enumerate(plan_features_data, start=1):
        features.append(
            PlanFeature(
                feature_id=feature_id,
                plan_id=plan_id,
                feature_name=feature_name
            )
        )
    
    return pd.DataFrame([feature.model_dump() for feature in features])


if __name__ == "__main__":
    df = generate_plan_features()
    print(f"Generated {len(df)} plan features")
    print(df.head(10))
    print(f"\nFeatures per plan:")
    print(df.groupby('plan_id').size())
