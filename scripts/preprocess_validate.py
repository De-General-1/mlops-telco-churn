import pandas as pd
from sklearn.preprocessing import StandardScaler
import joblib
import os

def preprocess_and_save(input_path='data/Telco-Customer-Churn.csv', output_path='data/processed.csv'):
    print("Loading data...")
    df = pd.read_csv(input_path)

    # Clean TotalCharges (convert to float, handle spaces/empty)
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')

    # Drop rows where Churn or TotalCharges is NaN
    df = df[df['Churn'].notna()]
    df = df[df['TotalCharges'].notna()]

    # Drop customerID
    df.drop(columns=['customerID'], inplace=True)

    # Encode target
    df['Churn'] = df['Churn'].map({'Yes': 1, 'No': 0})

    if df['Churn'].isnull().any():
        raise ValueError("Found unexpected values in Churn column that couldn't be mapped to 0/1.")

    # One-hot encode categorical features
    df = pd.get_dummies(df)

    # Split into features and target
    X = df.drop(columns=['Churn'])
    y = df['Churn']

    # Feature scaling
    scaler = StandardScaler()
    X_scaled = pd.DataFrame(scaler.fit_transform(X), columns=X.columns)

    # Combine with target
    df_processed = X_scaled.copy()
    df_processed['Churn'] = y.reset_index(drop=True)

    # Create folders
    os.makedirs('data', exist_ok=True)
    os.makedirs('models', exist_ok=True)

    # Save
    df_processed.to_csv(output_path, index=False)
    joblib.dump(scaler, 'models/scaler.joblib')

    print(f"Preprocessed data saved to {output_path}")
    print(f"Scaler saved to models/scaler.joblib")
    print(f"Final shape: {df_processed.shape}")
    print(f"Churn distribution:\n{df_processed['Churn'].value_counts()}")

if __name__ == "__main__":
    preprocess_and_save()
