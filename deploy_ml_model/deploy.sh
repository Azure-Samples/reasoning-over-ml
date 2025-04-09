#!/bin/bash

# Check for required commands
command -v az >/dev/null 2>&1 || { echo >&2 "az CLI is required but not installed. Aborting."; exit 1; }

### PARAMETERS ###
if [ -f ../.env ]; then
    # Source the .env file to load variables into the environment
    set -a
    . ../.env
    set +a
    # Assign the variables from .env (note: names are case-sensitive)
    location="${LOCATION}"
    resource_group="${AZURE_RESOURCE_GROUP}"
else
    echo ".env file not found. Please create it with the required variables."
    exit 1
fi

# <set_variables>
MODEL_NAME='forecasting-store-sales'
ml_workspace="${resource_group/-rg/}-ml"
echo ${ml_workspace}
subscription_id=$(az account show --query id --output tsv)

# Generate a unique endpoint name using the prefix
ENDPOINT_SUFFIX=$(date +"%Y%m")
ENDPOINT_NAME="${MODEL_NAME}-test" #${ENDPOINT_SUFFIX}"
DEPLOYMENT_NAME="forecasting-xgboost-mlflow"
DATA_ASSET_NAME="store-sales"
# </set_variables>

# <set_workspace>
az account set --subscription "$subscription_id"
az configure --defaults workspace="$ml_workspace" group="$resource_group"
# </set_workspace>

# <register_model>
#az ml model create --name "$MODEL_NAME" --type "mlflow_model" --path "deployment/model"
# </register_model>

# <create_data_asset>
#az ml data create -f store-dataset.yml
# </create_data_asset>

echo "Creating compute"
# <create_compute>
#az ml compute create -n batch-cluster --type amlcompute --min-instances 0 --max-instances 5
# </create_compute>


echo "Creating batch endpoint: $ENDPOINT_NAME"
# <create_endpoint>
az ml batch-endpoint create -n "$ENDPOINT_NAME" -f endpoint.yml
# </create_endpoint>

echo "Showing details of the batch endpoint"
# <query_endpoint>
az ml batch-endpoint show --name "$ENDPOINT_NAME"
# </query_endpoint>

echo "Creating batch deployment: $DEPLOYMENT_NAME for endpoint: $ENDPOINT_NAME"
# <create_deployment>
az ml batch-deployment create --file deployment/deployment.yml --endpoint-name "$ENDPOINT_NAME" --set-default
# </create_deployment>

echo "Setting traffic to 100% for deployment: $DEPLOYMENT_NAME"
# <set_traffic>
az ml batch-endpoint update --name "$ENDPOINT_NAME" --set "defaults.deployment_name=$DEPLOYMENT_NAME"



echo "Showing details of the batch deployment"
# <query_deployment>
az ml batch-deployment show --name "$DEPLOYMENT_NAME" --endpoint-name "$ENDPOINT_NAME"
# </query_deployment>



# Update environment variables in .env for later use without recreating the file
env_file="../.env"

if grep -q "^ENDPOINT_NAME=" "$env_file"; then
    sed -i "" "s/^ENDPOINT_NAME=.*/ENDPOINT_NAME=$ENDPOINT_NAME/" "$env_file"
else
    echo "ENDPOINT_NAME=$ENDPOINT_NAME" >> "$env_file"
fi

if grep -q "^WORKSPACE_NAME=" "$env_file"; then
    sed -i "" "s/^WORKSPACE_NAME=.*/WORKSPACE_NAME=$ml_workspace/" "$env_file"
else
    echo "WORKSPACE_NAME=$ml_workspace" >> "$env_file"
fi

if grep -q "^DATA_ASSET_NAME=" "$env_file"; then
    sed -i "" "s/^DATA_ASSET_NAME=.*/DATA_ASSET_NAME=$DATA_ASSET_NAME/" "$env_file"
else
    echo "DATA_ASSET_NAME=$DATA_ASSET_NAME" >> "$env_file"
fi

echo "Deployment script completed successfully."
