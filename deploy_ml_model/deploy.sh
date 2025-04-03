#!/bin/bash

# Check for required commands
command -v az >/dev/null 2>&1 || { echo >&2 "az CLI is required but not installed. Aborting."; exit 1; }

### PARAMETERS ###
if [ -f .env ]; then
    # Source the .env file to load variables into the environment
    set -a
    . .env
    set +a
    # Assign the variables from .env (note: names are case-sensitive)
    prefix="${PREFIX}"
    location="${LOCATION}"
else
    echo ".env file not found. Please create it with the required variables."
    exit 1
fi

# <set_variables>
ai_resource_name="$prefix"
resource_group="${ai_resource_name}-rg"
MODEL_NAME='forecasting-store-sales'
ml_workspace="${ai_resource_name}-ml"
subscription_id=$(az account show --query id --output tsv)

# Generate a unique endpoint name using the prefix
ENDPOINT_SUFFIX="$prefix"
ENDPOINT_NAME="${MODEL_NAME}-${ENDPOINT_SUFFIX}"
DEPLOYMENT_NAME="classifier-xgboost-mlflow"
# </set_variables>

# <set_workspace>
az account set --subscription "$subscription_id"
az configure --defaults workspace="$ml_workspace" group="$resource_group"
# </set_workspace>

# <register_model>
az ml model create --name "$MODEL_NAME" --type "mlflow_model" --path "deployment/model"
# </register_model>

# <create_data_asset>
az ml data create -f store-dataset.yml
# </create_data_asset>

echo "Creating compute"
# <create_compute>
az ml compute create -n batch-cluster --type amlcompute --min-instances 0 --max-instances 5
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
az ml batch-endpoint update --name "$ENDPOINT_NAME" --set "traffic.$DEPLOYMENT_NAME=100"
# </set_traffic>

echo "Updating the batch endpoint to set default deployment: $DEPLOYMENT_NAME"
# <set_default_deployment>
az ml batch-endpoint update --name "$ENDPOINT_NAME" --set "defaults.deployment_name=$DEPLOYMENT_NAME"
# </set_default_deployment>

echo "Showing details of the batch deployment"
# <query_deployment>
az ml batch-deployment show --name "$DEPLOYMENT_NAME" --endpoint-name "$ENDPOINT_NAME"
# </query_deployment>

# Save environment variables to .env for later use
{
    echo "ENDPOINT_NAME=$ENDPOINT_NAME";
    echo "WORKSPACE_NAME=$ml_workspace";
    echo "PREFIX=$prefix";
    echo "LOCATION=$location";
} >> .env

echo "Deployment script completed successfully."
