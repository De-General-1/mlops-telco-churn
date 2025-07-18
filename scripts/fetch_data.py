import boto3
import os

def fetch_data(bucket_name, s3_key, local_path='data/Telco-Customer-Churn.csv', profile_name='default'):
    session = boto3.Session(profile_name=profile_name)
    s3 = session.client('s3')

    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    s3.download_file(bucket_name, s3_key, local_path)
    print(f"Downloaded s3://{bucket_name}/{s3_key} to {local_path}")

if __name__ == "__main__":
    fetch_data(
        bucket_name='phase3-mlops-source-bucket-degen-1',
        s3_key='datasets/Telco-Customer-Churn.csv',
        profile_name='degen-mlops'
    )
