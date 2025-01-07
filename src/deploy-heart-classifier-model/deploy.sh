#!/bin/bash
### PARAMETERS ###
prefix="demo-reasoning-o1-ml"                                # The prefix for the resources
location="eastus2"

# <set_variables>
ai_resource_name="$prefix"
ai_resource_name_resource_group_name=$ai_resource_name"-rg"
export ENDPOINT_NAME=$ai_resource_name"-ep"
ai_resource_name_aml_name=$ai_resource_name"-ml"
subscription_id=$(az account show --query id --output tsv)
# </set_variables>

# <set_workspace>
az account set --subscription $subscription_id
az configure --defaults workspace=$ai_resource_name_aml_name group=$ai_resource_name_resource_group_name
# </set_workspace>

# <name_endpoint>
ENDPOINT_NAME="heart-classifier"
# </name_endpoint>

# The following code ensures the created deployment has a unique name
ENDPOINT_SUFIX=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w ${1:-5} | head -n 1)
ENDPOINT_NAME="$ENDPOINT_NAME-$ENDPOINT_SUFIX"


# <register_model>
MODEL_NAME='heart-classifier-mlflow'
az ml model create --name $MODEL_NAME --type "mlflow_model" --path "deployment-simple/model"
# </register_model>

# <create_data_asset>
az ml data create -f heart-dataset-unlabeled.yml
# </create_data_asset>

echo "Creating compute"
# <create_compute>
az ml compute create -n batch-cluster --type amlcompute --min-instances 0 --max-instances 5
# </create_compute>

echo "Creating batch endpoint $ENDPOINT_NAME"
# <create_endpoint>
az ml batch-endpoint create -n $ENDPOINT_NAME -f endpoint.yml
# </create_endpoint>

echo "Showing details of the batch endpoint"
# <query_endpoint>
az ml batch-endpoint show --name $ENDPOINT_NAME
# </query_endpoint>

echo "Creating batch deployment $DEPLOYMENT_NAME for endpoint $ENDPOINT_NAME"
# <create_deployment>
az ml batch-deployment create --file deployment-simple/deployment.yml --endpoint-name $ENDPOINT_NAME --set-default
# </create_deployment>

echo "Update the batch deployment as default for the endpoint"
# <set_default_deployment>
DEPLOYMENT_NAME="classifier-xgboost-mlflow"
az ml batch-endpoint update --name $ENDPOINT_NAME --set defaults.deployment_name=$DEPLOYMENT_NAME
# </set_default_deployment>

echo "Showing details of the batch deployment"
# <query_deployment>
az ml batch-deployment show --name $DEPLOYMENT_NAME --endpoint-name $ENDPOINT_NAME
# </query_deployment>
