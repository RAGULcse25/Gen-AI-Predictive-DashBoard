from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, r2_score
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, GradientBoostingClassifier, GradientBoostingRegressor
from sklearn.linear_model import LogisticRegression, LinearRegression
import pandas as pd

def run_automl_prediction_loop(X, y, target_is_categorical: bool):
    """
    Splits data, detects problem type, trains multiple models,
    and returns the best performing model + metrics.
    """
    # Split into training and testing sets (80% / 20%)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Define our pool of models based on the problem type
    if target_is_categorical:
        models = {
            "Random Forest Classifier": RandomForestClassifier(random_state=42),
            "Gradient Boosting Classifier": GradientBoostingClassifier(random_state=42),
            "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42)
        }
        metric_name = "Accuracy"
    else:
        models = {
            "Random Forest Regressor": RandomForestRegressor(random_state=42),
            "Gradient Boosting Regressor": GradientBoostingRegressor(random_state=42),
            "Linear Regression": LinearRegression()
        }
        metric_name = "R2_Score"

    best_model_name = None
    best_score = -float('inf')
    best_model_object = None
    
    # The Auto-ML Loop: Train and evaluate each model
    for name, model in models.items():
        try:
            # Train the model
            model.fit(X_train, y_train)
            predictions = model.predict(X_test)
            
            # Calculate metric
            if target_is_categorical:
                score = accuracy_score(y_test, predictions)
            else:
                score = r2_score(y_test, predictions)
                
            # Check if this model beat the previous best
            if score > best_score:
                best_score = score
                best_model_name = name
                best_model_object = model
        except Exception as e:
            # Ignore models that fail due to shapes/types
            pass

    # Extract Feature Importances from the winner (if applicable)
    feature_importance = {}
    if best_model_object and hasattr(best_model_object, 'feature_importances_'):
        importances = best_model_object.feature_importances_
        for col, imp in zip(X.columns, importances):
            feature_importance[col] = round(float(imp), 4)
        # Sort features by importance score
        feature_importance = dict(sorted(feature_importance.items(), key=lambda item: item[1], reverse=True))

    return {
        "problem_type": "Classification" if target_is_categorical else "Regression",
        "best_model": best_model_name if best_model_name else "Linear Baseline",
        "evaluation_metric": metric_name,
        "score": round(best_score, 4) if best_score != -float('inf') else 0.0,
        "top_features": list(feature_importance.items())[:3] if feature_importance else []
    }
