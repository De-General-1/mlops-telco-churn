import great_expectations as ge
from great_expectations.core.batch import BatchRequest
import pandas as pd

def validate_data(path="data/processed.csv"):
    df = ge.from_pandas(pd.read_csv(path))

    # Define expectations
    df.expect_column_values_to_not_be_null("Churn")
    df.expect_column_values_to_be_in_set("Churn", [0, 1])
    df.expect_table_row_count_to_be_between(6000, 8000)
    df.expect_column_values_to_not_be_null("tenure")
    df.expect_column_to_exist("MonthlyCharges")

    # Run validation
    results = df.validate()

    if not results["success"]:
        raise ValueError("Data validation failed")

    print("Data validation passed ")

if __name__ == "__main__":
    validate_data()
