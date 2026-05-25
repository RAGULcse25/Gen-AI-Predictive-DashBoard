import pandas as pd
from sklearn.preprocessing import LabelEncoder

def clean_data_for_viz(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans missing values and duplicates for display/visualization.
    Does not encode categorical fields, keeping them human-readable.
    """
    cleaned_df = df.copy()
    
    # Remove exact duplicates
    cleaned_df = cleaned_df.drop_duplicates()
    
    # Handle missing values
    for col in cleaned_df.columns:
        if cleaned_df[col].isnull().any():
            if cleaned_df[col].dtype in ['int64', 'float64']:
                # Fill missing numbers with the median
                median_val = cleaned_df[col].median()
                cleaned_df[col] = cleaned_df[col].fillna(median_val)
            else:
                # Fill missing text categories with 'Unknown'
                cleaned_df[col] = cleaned_df[col].fillna('Unknown')
                
    return cleaned_df

def prepare_data_for_ml(df: pd.DataFrame, target_column: str):
    """
    Prepares the dataset for machine learning by encoding categorical columns and splitting features (X) and target (y).
    """
    cleaned_df = clean_data_for_viz(df)
    
    # Separate features and target
    y = cleaned_df[target_column]
    X = cleaned_df.drop(columns=[target_column])
    
    # Detect target type
    target_is_categorical = y.dtype == 'object' or y.dtype == 'category' or y.dtype == 'bool'
    
    # Encode target if categorical
    le = None
    if target_is_categorical:
        le = LabelEncoder()
        y = le.fit_transform(y.astype(str))
        
    # Convert date columns to numerical timestamp features for ML
    for col in X.columns:
        if X[col].dtype == 'object':
            # Check if it can be converted to datetime
            try:
                temp_date = pd.to_datetime(X[col], errors='raise', format='mixed')
                # Extract date features
                X[f'{col}_year'] = temp_date.dt.year
                X[f'{col}_month'] = temp_date.dt.month
                X[f'{col}_day'] = temp_date.dt.day
                X = X.drop(columns=[col])
            except:
                pass
                
    # One-hot encode categorical features
    X_encoded = pd.get_dummies(X, drop_first=True)
    
    return X_encoded, y, target_is_categorical, le
