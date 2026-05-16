# model.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import numpy as np

def train_lead_time_model(df):
    """Trains a Random Forest model to predict shipping lead times."""
    
    feature_cols = ['Origin Factory', 'Region', 'Ship Mode', 'Division', 
                    'Shipping Distance', 'Ship Mode Rank']
    
    X = df[feature_cols].copy()
    y = df['Lead Time'].copy()
    
    # Identify column types
    categorical_cols = ['Origin Factory', 'Region', 'Ship Mode', 'Division']
    numeric_cols = ['Shipping Distance', 'Ship Mode Rank']
    
    # Create preprocessing steps
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numeric_cols),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols)
        ])
    
    # Define the Pipeline with RandomForest
    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(
            n_estimators=100, 
            max_depth=10,
            min_samples_split=5,
            random_state=42
        ))
    ])
    
    # Train/Test Split & Fit
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate
    preds = model.predict(X_test)
    mae = mean_absolute_error(y_test, preds)
    r2 = r2_score(y_test, preds)
    rmse = np.sqrt(np.mean((y_test - preds) ** 2))
    
    metrics = {
        "MAE": mae, 
        "R2": r2, 
        "RMSE": rmse,
        "train_size": len(X_train),
        "test_size": len(X_test)
    }
    
    return model, metrics