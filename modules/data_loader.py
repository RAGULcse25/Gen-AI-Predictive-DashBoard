import pandas as pd
import io

def load_dataset(file_contents: bytes, filename: str) -> pd.DataFrame:
    """
    Loads dataset from bytes into a Pandas DataFrame based on file extension.
    """
    if filename.endswith('.csv'):
        return pd.read_csv(io.BytesIO(file_contents))
    elif filename.endswith(('.xlsx', '.xls')):
        return pd.read_excel(io.BytesIO(file_contents))
    else:
        raise ValueError("Unsupported file format. Please upload CSV or Excel.")

def inspect_dataset(df: pd.DataFrame, filename: str) -> dict:
    """
    Inspects the dataset and returns metadata (shape, column types, guessed target).
    """
    total_rows, total_cols = df.shape

    # Separate Numerical and Categorical columns
    numerical_cols = df.select_dtypes(include=['number']).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category', 'bool']).columns.tolist()

    # Smart Target Variable Guessing Logic
    target_keywords = ['target', 'label', 'output', 'score', 'grade', 'sales', 'revenue', 'status', 'outcome', 'price', 'churn', 'profit']
    guessed_target = None
    
    for col in df.columns:
        if any(keyword in col.lower() for keyword in target_keywords):
            guessed_target = col
            break
            
    if not guessed_target and len(df.columns) > 0:
        guessed_target = df.columns[-1]

    return {
        "filename": filename,
        "rows": total_rows,
        "columns_count": total_cols,
        "numerical_columns": numerical_cols,
        "categorical_columns": categorical_cols,
        "guessed_target": guessed_target,
        "all_columns": df.columns.tolist()
    }
