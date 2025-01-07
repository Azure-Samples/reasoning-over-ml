import pytest
import pandas as pd
import os

def test_validate_schema():
    # Load the output CSV file
    output_df= pd.read_csv(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src', 'deploy_ml_model', 'data', 'output.csv'))

    # Extract the column names
    output_columns = output_df.columns.tolist()

    # Validate if output_df has the required columns
    required_columns = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal']
    for column in required_columns:
        assert column in output_columns, f"Required column {column} is missing from output columns"
