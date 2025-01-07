import json
import os
from dotenv import load_dotenv

from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential
from azure.ai.ml.entities import Data

def create_input_data_for_model():
    # Load environment variables from a .env file
    load_dotenv()

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
        config_path = "../.azureml/config.json"
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, "w") as fo:
            fo.write(json.dumps(client_config))
        ml_client = MLClient.from_config(credential=credential, path=config_path)

    print("Creating input data asset for model...")
    
    # Create a data asset
    data_asset = Data(
        name="output_data_asset",
        path=r"..\gbbai-o1-reasoning-over-ml\src\deploy-ml-model\data",
        type="uri_folder",
        description="Data asset for output data",
        tags={"source": "output"}
    )

    # Register the data asset
    ml_client.data.create_or_update(data_asset)
