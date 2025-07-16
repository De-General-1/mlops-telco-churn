import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import train_test_split
import mlflow
import mlflow.sklearn
import joblib
import os

def train_and_log(data_path='data/processed.csv'):
    df = pd.read_csv(data_path)
    X = df.drop('Churn', axis=1)
    y = df['Churn']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred),
        "recall": recall_score(y_test, y_pred),
        "f1": f1_score(y_test, y_pred),
        "roc_auc": roc_auc_score(y_test, y_pred),
    }

    # Start MLflow run
    with mlflow.start_run():
        mlflow.log_params({"model_type": "LogisticRegression", "max_iter": 1000})
        mlflow.log_metrics(metrics)
        mlflow.sklearn.log_model(model, artifact_path="model")
        joblib.dump(model, "models/churn_model.joblib")
        print(f"Model trained and logged to MLflow")

if __name__ == "__main__":
    train_and_log()
