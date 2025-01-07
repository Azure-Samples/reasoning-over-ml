#!/bin/bash
### PARAMETERS ###
prefix="demo-reasoning-o1-ml"                                # The prefix for the resources
location="eastus2"
### END OF PARAMETERS ###

### Get the subscription id and the user id
subscription_id=$(az account show --query id --output tsv)
user_id=$(az ad signed-in-user show --query id --output tsv)

# <set_variables>
ai_resource_name="$prefix"
ai_resource_name_resource_group_name=$ai_resource_name"-rg"
ai_resource_name_hub_name=$ai_resource_name"-hub"
ai_resource_name_aml_name=$ai_resource_name"-ml"
ai_resource_project_name=$ai_resource_name"-project"
ai_resource_ai_service=$ai_resource_name"-aiservice"
# </set_variables>


function create_resource_group() {
    echo "Creating resource group: $ai_resource_name_resource_group_name"
    az group create --name $ai_resource_name_resource_group_name --location $location > null
}

function create_hub() {
    echo "Creating AI Studio Hub: $ai_resource_name_hub_name"
    az ml workspace create --kind hub --resource-group $ai_resource_name_resource_group_name --name $ai_resource_name_hub_name > null
}

function create_workspace() {
    echo "Creating Azure Machine Learning Workspace: $ai_resource_name_aml_name"
    az ml workspace create --name $ai_resource_name_aml_name --resource-group $ai_resource_name_resource_group_name --location $location > null
}

function create_project() {
    hub_id=$(az ml workspace show -g $ai_resource_name_resource_group_name --name $ai_resource_name_hub_name --query id --output tsv)
    echo "Creating AI Studio Project: $ai_resource_project_name"
    az ml workspace create --kind project --resource-group $ai_resource_name_resource_group_name --name $ai_resource_project_name --hub-id $hub_id > null
}

function create_ai_service() {
    echo "Creating AI Service Account: $ai_resource_ai_service"
    az cognitiveservices account purge -l $location -n $ai_resource_ai_service -g $ai_resource_name_resource_group_name
    az cognitiveservices account create --kind AIServices --location $location --name $ai_resource_ai_service --resource-group $ai_resource_name_resource_group_name --sku S0 --yes > null
}

function deploy_models() {
    echo "Deploying GPT-4o"
    az cognitiveservices account deployment create --name $ai_resource_ai_service --resource-group $ai_resource_name_resource_group_name --deployment-name "gpt-4o" --model-name "gpt-4o" --model-version "2024-05-13" --model-format "OpenAI" --sku-capacity "1" --sku-name "Standard" #--capacity "100"

    #echo "Deploying GPT-o1-preview"
    #az cognitiveservices account deployment create --name $ai_resource_ai_service --resource-group $ai_resource_name_resource_group_name --deployment-name "text-embedding-ada-002" --model-name "text-embedding-ada-002" --model-format "OpenAI" --model-version "2" --sku-capacity "1" --sku-name "Standard" --capacity "20"
}

function add_connection_to_hub() {
    echo "Adding AI Service Connection to the HUB"
    ai_service_resource_id=$(az cognitiveservices account show --name $ai_resource_ai_service --resource-group $ai_resource_name_resource_group_name --query id --output tsv)
    ai_service_api_key=$(az cognitiveservices account keys list --name $ai_resource_ai_service --resource-group $ai_resource_name_resource_group_name --query key1 --output tsv)

    rm connection.yml
    echo "name: $ai_resource_ai_service" >> connection.yml
    echo "type: azure_ai_services" >> connection.yml
    echo "endpoint: https://$location.api.cognitive.microsoft.com/" >> connection.yml
    echo "api_key: $ai_service_api_key" >> connection.yml
    echo "ai_services_resource_id:  $ai_service_resource_id" >> connection.yml

    az ml connection create --file connection.yml --resource-group $ai_resource_name_resource_group_name --workspace-name $ai_resource_name_hub_name > null
    rm connection.yml
    az role assignment create --role "Storage Blob Data Contributor" --scope subscriptions/$subscription_id/resourceGroups/$ai_resource_name_resource_group_name --assignee-principal-type User --assignee-object-id $user_id
}


function create_env(){    echo "Creating .env file"
    echo "# Please do not share this file, or commit this file to the repository" > .env
    echo "# This file is used to store the environment variables for the project for demos and testing only" >> .env
    echo "# delete this file when done with demos, or if you are not using it" >> .env
    echo "AZURE_OPENAI_ENDPOINT=https://$location.api.cognitive.microsoft.com/" >> .env
    echo "AZURE_OPENAI_KEY=$ai_service_api_key" >> .env
    echo 'AZURE_OPENAI_API_VERSION="2024-08-01-preview"' >> .env
    echo 'AZURE_OPENAI_MODEL_NAME="gpt-4o"' >> .env
    echo "AZURE_SUBSCRIPTION_ID=$subscription_id" >> .env
    echo "AZURE_RESOURCE_GROUP=$ai_resource_name_resource_group_name" >> .env
}

function run_all() {
    create_resource_group
    create_hub
    create_workspace
    create_project
    create_ai_service
    deploy_models
    add_connection_to_hub
    create_env
}

case $1 in
    create_resource_group)
        create_resource_group
        ;;
    create_hub)
        create_hub
        ;;
    create_project)
        create_project
        ;;
    create_ai_service)
        create_ai_service
        ;;
    deploy_models)
        deploy_models
        ;;
    add_connection_to_hub)
        add_connection_to_hub
        ;;
    run_all)
        run_all
        ;;
    *)
        echo "Usage: $0 {create_resource_group|create_hub|create_project|create_ai_service|deploy_models|add_connection_to_hub|run_all}"
        exit 1
        ;;
esac