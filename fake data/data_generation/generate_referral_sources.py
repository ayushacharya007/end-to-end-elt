"""
Generate referral sources lookup table
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
from models import ReferralSource


def generate_referral_sources() -> pd.DataFrame:
    """
    Generate static referral sources reference table
    
    Returns:
        DataFrame with referral_source_id, source_name
    """
    referral_sources = [
        ReferralSource(referral_source_id=1, source_name='web search'),
        ReferralSource(referral_source_id=2, source_name='paid ads'),
        ReferralSource(referral_source_id=3, source_name='social media'),
        ReferralSource(referral_source_id=4, source_name='friend'),
    ]
    
    return pd.DataFrame([source.model_dump() for source in referral_sources])


if __name__ == "__main__":
    df = generate_referral_sources()
    print(f"Generated {len(df)} referral sources")
    print(df)
