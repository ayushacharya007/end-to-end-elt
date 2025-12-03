"""
Generate payment methods lookup table
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
from models import PaymentMethod


def generate_payment_methods() -> pd.DataFrame:
    """
    Generate static payment methods reference table
    
    Returns:
        DataFrame with payment_method_id, method_name
    """
    payment_methods = [
        PaymentMethod(payment_method_id=1, method_name='credit card'),
        PaymentMethod(payment_method_id=2, method_name='paypal'),
        PaymentMethod(payment_method_id=3, method_name='bank transfer'),
        PaymentMethod(payment_method_id=4, method_name='N/A'),  # For free plans
    ]
    
    return pd.DataFrame([method.model_dump() for method in payment_methods])


if __name__ == "__main__":
    df = generate_payment_methods()
    print(f"Generated {len(df)} payment methods")
    print(df)
