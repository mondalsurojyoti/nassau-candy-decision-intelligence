# data_prep.py
import pandas as pd
import numpy as np
from haversine import haversine
from config import FACTORIES, PRODUCT_MAPPING, REGION_CENTERS

def calculate_distance(factory_name, region):
    """Calculates Haversine distance between a factory and a region center."""
    if factory_name not in FACTORIES or region not in REGION_CENTERS:
        return 1000 # Default fallback distance
    
    fac_coords = (FACTORIES[factory_name]["lat"], FACTORIES[factory_name]["lon"])
    reg_coords = (REGION_CENTERS[region]["lat"], REGION_CENTERS[region]["lon"])
    return haversine(fac_coords, reg_coords)

def load_and_prep_data(filepath="Nassau Candy Distributor.csv"):
    """Loads CSV, cleans data, and engineers features for modeling."""
    try:
        df = pd.read_csv(filepath)
    except FileNotFoundError:
        return None 
    
    # 1. Date Math to create our Target Variable: Lead Time
    df['Order Date'] = pd.to_datetime(df['Order Date'], format='mixed', dayfirst=True)
    df['Ship Date'] = pd.to_datetime(df['Ship Date'], format='mixed', dayfirst=True)
    df['Lead Time'] = (df['Ship Date'] - df['Order Date']).dt.days
    
    # Clean anomalies (e.g., negative lead times)
    df = df[df['Lead Time'] >= 0]
    
    # 2. Assign Current Factory based on Product Name
    df['Origin Factory'] = df['Product Name'].map(PRODUCT_MAPPING)
    
    # 3. Calculate Estimated Shipping Distance
    df['Shipping Distance'] = df.apply(
        lambda row: calculate_distance(row['Origin Factory'], row['Region']), axis=1
    )
    
    # 4. Encode Ship Mode as ordinal (speed ranking)
    ship_mode_rank = {'Same Day': 0, 'First Class': 1, 'Second Class': 2, 'Standard Class': 3}
    df['Ship Mode Rank'] = df['Ship Mode'].map(ship_mode_rank).fillna(3)
    
    # 5. Keep financial columns for KPI calculations
    features = ['Origin Factory', 'Region', 'Ship Mode', 'Division', 
                'Shipping Distance', 'Ship Mode Rank']
    target = 'Lead Time'
    extra_cols = ['Product Name', 'Sales', 'Gross Profit', 'Cost', 'Units']
    
    keep_cols = features + [target] + [c for c in extra_cols if c in df.columns]
    return df[keep_cols].dropna()