import boto3
import os

def upload_to_s3(local_path, bucket_name, s3_key, profile_name='default'):
    session = boto3.Session(profile_name=profile_name)
    s3 = session.client('s3')
    
    if not os.path.exists(local_path):
        raise FileNotFoundError(f"{local_path} does not exist.")

    s3.upload_file(local_path, bucket_name, s3_key)
    print(f"Uploaded {local_path} to s3://{bucket_name}/{s3_key}")

if __name__ == "__main__":
    upload_to_s3(
        local_path='data/Telco-Customer-Churn.csv',
        bucket_name='phase3-mlops-source-bucket-degen-1',
        s3_key='datasets/Telco-Customer-Churn.csv',
        profile_name='degen-mlops'
    )
