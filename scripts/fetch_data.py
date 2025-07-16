import os
import pandas as pd

def fetch_data(local_path='data/Telco-Customer-Churn.csv'):
    url = "https://raw.githubusercontent.com/blastchar/telco-customer-churn/master/WA_Fn-UseC_-Telco-Customer-Churn.csv"
    os.makedirs('data', exist_ok=True)
    df = pd.read_csv(url)
    df.to_csv(local_path, index=False)
    print(f" Data saved to {local_path}")

if __name__ == "__main__":
    fetch_data()
