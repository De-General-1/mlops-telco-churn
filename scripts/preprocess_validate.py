import pandas as pd
from sklearn.preprocessing import StandardScaler
import joblib
import os

def preprocess_and_save(input_path='data/Telco-Customer-Churn.csv', output_path='data/processed.csv'):
    df = pd.read_csv(input_path)

    # Clean 'TotalCharges'
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    df.dropna(inplace=True)

    # Drop unnecessary columns
    df.drop(['customerID'], axis=1, inplace=True)

    # Encode target
    df['Churn'] = df['Churn'].map({'Yes': 1, 'No': 0})

    # One-hot encode categorical features
    df = pd.get_dummies(df)

    # Feature scaling
    scaler = StandardScaler()
    features = df.drop('Churn', axis=1)
    df_scaled = pd.DataFrame(scaler.fit_transform(features), columns=features.columns)
    df_scaled['Churn'] = df['Churn']

    # Save preprocessed data and scaler
    os.makedirs('data', exist_ok=True)
    df_scaled.to_csv(output_path, index=False)
    joblib.dump(scaler, 'models/scaler.joblib')
    print(f"Preprocessed data saved to {output_path}")

if __name__ == "__main__":
    preprocess_and_save()
