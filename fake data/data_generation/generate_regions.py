"""
Generate regions lookup table
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
from models import Region


def generate_regions() -> pd.DataFrame:
    """
    Generate static regions reference table
    
    Returns:
        DataFrame with region_id, region_name
    """
    regions = [
        Region(region_id=1, region_name='North America'),
        Region(region_id=2, region_name='Europe'),
        Region(region_id=3, region_name='Asia'),
        Region(region_id=4, region_name='South America'),
        Region(region_id=5, region_name='Africa'),
        Region(region_id=6, region_name='Oceania'),
    ]
    
    return pd.DataFrame([region.model_dump() for region in regions])


if __name__ == "__main__":
    df = generate_regions()
    print(f"Generated {len(df)} regions")
    print(df)
