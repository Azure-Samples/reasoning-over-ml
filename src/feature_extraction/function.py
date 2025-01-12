import requests
import json
import os
import logging
from dotenv import load_dotenv

from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential
from azure.ai.ml import Input

import time
import pandas as pd
import glob
import json, os

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load environment variables from a .env file
load_dotenv()
ENDPOINT_NAME = os.getenv("ENDPOINT_NAME")
LOCATION = os.getenv("LOCATION")
WORKSPACE_NAME = os.getenv("WORKSPACE_NAME")


client_config = {
    "subscription_id": os.getenv("SUBSCRIPTION_ID"),
    "resource_group": os.getenv("AZURE_RESOURCE_GROUP"),
    "workspace_name": os.getenv("WORKSPACE_NAME"),
}

# write and reload from config file
config_path = "../.azureml/config.json"
os.makedirs(os.path.dirname(config_path), exist_ok=True)
with open(config_path, "w") as fo:
    fo.write(json.dumps(client_config))

# Get the data asset path
credential = DefaultAzureCredential()

# Get access token
access_token = credential.get_token("https://ml.azure.com/.default")
if access_token:
    access_token = access_token.token
else:
    logging.error("Failed to retrieve access token.")


ml_client = MLClient.from_config(credential=credential, path=config_path)


def get_output(job_name):
    ml_client.jobs.download(
        name=job_name, download_path="./results_invoke", output_name="score"
    )
    output_files = glob.glob("./results_invoke/*.csv")
    score = pd.concat((pd.read_csv(f) for f in output_files))
    return score


def invoke_endpoint():
    data_asset = ml_client.data.get("heart-dataset-unlabeled", version="2")

    path = data_asset.path
    logging.info(f"Data asset path: {path}")

    # Replace with your Azure Machine Learning endpoint URL
    url = f"https://{ENDPOINT_NAME}.{LOCATION}.inference.ml.azure.com/jobs"

    # Headers to include the access token for authorization
    headers = {
        "Authorization": f"Bearer <{access_token}>",
        "Content-Type": "application/json",
    }

    # Example payload for a batch request (structure depends on your model input)
    data = {
        "properties": {
            "InputData": {
                "heart_data": {
                    "JobInputType": "UriFolder",
                    "Uri": path,
                }
            }
        }
    }

    # Make a POST request to submit the batch job
    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 202:
        logging.info("Batch job submitted successfully!")
        logging.info(response.json())  # Print response from the service
    else:
        logging.error(f"Error: {response.status_code}")
        logging.error(response.text)

    job_name = response.json()["name"]

    # Construct the URL to get the job status
    status_url = (
        f"https://{ENDPOINT_NAME}.{LOCATION}.inference.ml.azure.com/jobs/{job_name}"
    )

    # Poll the job status until it is completed
    while True:
        status_response = requests.get(status_url, headers=headers)
        status = status_response.json()["properties"]["status"]
        if status in ["Completed", "Failed"]:
            break
        logging.info(
            f"Job status: {status}. Waiting for 10 seconds before checking again..."
        )
        time.sleep(10)

    if status == "Completed":
        if status_response.status_code == 200:
            logging.info("Job output retrieved successfully!")
            score = get_output(job_name)
        else:
            logging.error(f"Error retrieving job output: {status_response.status_code}")
            logging.error(status_response.text)
            raise Exception(
                f"Error retrieving job output: {status_response.status_code}"
            )
        return score
    else:
        logging.error(f"Job failed with status: {status}")
        logging.error(status_response.json())
        raise Exception(f"Job failed with status: {status}")




def invoke_endpoint_sdk():
    data_asset = ml_client.data.get("heart-dataset-unlabeled", version="2")

    path = data_asset.path
    logging.info(f"Data asset path: {path}")
    

    job = ml_client.batch_endpoints.invoke(
        ENDPOINT_NAME,
        inputs={"heart_data": Input(path=path)}
    )

    job_name = job.name
    time.sleep(1)
    job = ml_client.jobs.get(job_name)
    logging.info(f"Job name: {job_name}")

    while True:
        status = job.status
        if status in ["Completed", "Failed"]:
            break
        logging.info(
            f"Job status: {status}. Waiting for 10 seconds before checking again..."
        )
        time.sleep(10)

    if status == "Completed":
        logging.info("Job completed successfully!")
        score = get_output(job_name)
        return score
    else:
        logging.error(f"Job failed with status: {status}")
        raise Exception(f"Job failed with status: {status}")

