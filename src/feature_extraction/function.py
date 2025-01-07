import requests
import json
import os
from dotenv import load_dotenv

from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential
import time

# Load environment variables from a .env file
load_dotenv()
ENDPOINT_NAME = os.getenv("ENDPOINT_NAME")
LOCATION = os.getenv("LOCATION")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")


# Get the data asset path
credential = DefaultAzureCredential()
try:
    ml_client = MLClient.from_config(credential=credential)
except Exception as ex:
    # NOTE: Update following workspace information to contain
    #       your subscription ID, resource group name, and workspace name
    client_config = {
        "subscription_id": os.getenv("SUBSCRIPTION_ID"),
        "resource_group": os.getenv("AZURE_RESOURCE_GROUP"),
        "workspace_name": os.getenv("WORKSPACE_NAME"),
    }

    # write and reload from config file
    import json, os

    config_path = "../.azureml/config.json"
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    with open(config_path, "w") as fo:
        fo.write(json.dumps(client_config))
    ml_client = MLClient.from_config(credential=credential, path=config_path)


data_asset = ml_client.data.get("heart-dataset-unlabeled", version="2")

path = data_asset.path
print(path)


# Replace with your Azure Machine Learning endpoint URL
url = f"https://{ENDPOINT_NAME}.{LOCATION}.inference.ml.azure.com/jobs"

# Headers to include the access token for authorization
headers = {
    "Authorization": f"Bearer <{ACCESS_TOKEN}>",
    "Content-Type": "application/json",
}

# Example payload for a batch request (structure depends on your model input)
data = {
    "properties": {
        "InputData": {"heart_data": {"JobInputType": "UriFolder", "Uri": path}}
    }
}


# Make a POST request to submit the batch job
response = requests.post(url, headers=headers, data=json.dumps(data))

if response.status_code == 202:
    print("Batch job submitted successfully!")
    print(response.json())  # Print response from the service
else:
    print(f"Error: {response.status_code}")
    print(response.text)





    # Extract job ID from the response
    job_id = response.json()["id"]

    # Construct the URL to get the job status
    status_url = f"https://{ENDPOINT_NAME}.{LOCATION}.inference.ml.azure.com/jobs/{job_id}"

    # Poll the job status until it is completed

    while True:
        status_response = requests.get(status_url, headers=headers)
        status = status_response.json()["properties"]["status"]
        if status in ["Completed", "Failed"]:
            break
        print(f"Job status: {status}. Waiting for 10 seconds before checking again...")
        time.sleep(10)

    if status == "Completed":
        # Construct the URL to get the job output
        output_url = f"https://{ENDPOINT_NAME}.{LOCATION}.inference.ml.azure.com/jobs/{job_id}/outputs"
        output_response = requests.get(output_url, headers=headers)
        if output_response.status_code == 200:
            print("Job output retrieved successfully!")
            print(output_response.json())  # Print the job output
        else:
            print(f"Error retrieving job output: {output_response.status_code}")
            print(output_response.text)
    else:
        print(f"Job failed with status: {status}")
        print(status_response.json())