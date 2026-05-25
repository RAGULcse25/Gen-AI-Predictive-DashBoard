from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, r2_score

# Import a mix of Classification and Regression models
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, GradientBoostingClassifier, GradientBoostingRegressor
from sklearn.linear_model import LogisticRegression, LinearRegression

def run_automl_prediction_loop(X, y, target_is_categorical: bool):
    """
    Splits the data, detects problem type, trains multiple models,
    and returns the best performing model + metrics.
    """
    # 1. Split into Training and Testing sets (80% / 20%)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 2. Define our competitive pool of models based on the problem type
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
    
    # 3. The Auto-ML Loop: Train and evaluate each model
    for name, model in models.items():
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

    # 4. Extract Feature Importances from the winner (if applicable)
    feature_importance = {}
    if hasattr(best_model_object, 'feature_importances_'):
        importances = best_model_object.feature_importances_
        for col, imp in zip(X.columns, importances):
            feature_importance[col] = round(float(imp), 4)
        # Sort features by importance score
        feature_importance = dict(sorted(feature_importance.items(), key=lambda item: item[1], reverse=True))

    # 5. Return payload for the dashboard and the GenAI prompt
    return {
        "problem_type": "Classification" if target_is_categorical else "Regression",
        "best_model": best_model_name,
        "evaluation_metric": metric_name,
        "score": round(best_score, 4),
        "top_features": list(feature_importance.items())[:3] # Top 3 most important columns
    }