import os
import pandas as pd
import joblib
import mlflow
import mlflow.sklearn

import dagshub
dagshub.init(repo_owner='De-General-1', repo_name='mlops-telco-churn', mlflow=True)
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import train_test_split
from mlflow.models.signature import infer_signature

def train_and_log(data_path='data/processed.csv'):
    # Load data
    df = pd.read_csv(data_path)
    X = df.drop('Churn', axis=1)
    y = df['Churn']

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train model
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    # Predict and calculate metrics
    y_pred = model.predict(X_test)
    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred),
        "recall": recall_score(y_test, y_pred),
        "f1": f1_score(y_test, y_pred),
        "roc_auc": roc_auc_score(y_test, y_pred),
    }

    # Prepare MLflow
    mlflow.set_experiment("telco-churn-prediction")

    with mlflow.start_run():
        # Log parameters and metrics
        mlflow.log_params({"model_type": "LogisticRegression", "max_iter": 1000})
        mlflow.log_metrics(metrics)

        # Infer and log model signature
        signature = infer_signature(X_train, model.predict(X_train))

        # Log the model
        mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path="model",
            registered_model_name="TelcoChurnModel",
            signature=signature,
            input_example=X_train.iloc[:5]
        )

        # Save model locally
        os.makedirs("models", exist_ok=True)
        joblib.dump(model, "models/churn_model.joblib")

        print("Model trained, logged to MLflow, and saved locally.")

if __name__ == "__main__":
    train_and_log()
