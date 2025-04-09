envFilePath="../../.env"

if [ -f "$envFilePath" ]; then
    rm -f "$envFilePath"
fi
touch "$envFilePath"
#!/bin/bash


# Add comments to the .env file
echo "# Please do not share this file, or commit this file to the repository" >> "$envFilePath"
echo "# This file is used to store the environment variables for the project for demos and testing only" >> "$envFilePath"
echo "# Delete this file when done with demos, or if you are not using it" >> "$envFilePath"

echo "LOCATION=$(azd env get-value AZURE_LOCATION)" >> "$envFilePath"
echo "RESOURCE_GROUP=$(azd env get-value RESOURCE_GROUP)" >> "$envFilePath"
echo "AZURE_OPENAI_MODEL_NAME=$(azd env get-value AZURE_OPENAI_MODEL_NAME)" >> "$envFilePath"
echo "AZURE_OPENAI_API_VERSION=$(azd env get-value AZURE_OPENAI_API_VERSION)" >> "$envFilePath"
echo "AZURE_OPENAI_ENDPOINT=$(azd env get-value AZURE_OPENAI_ENDPOINT)" >> "$envFilePath"
echo "SUBSCRIPTION_ID=$(azd env get-value SUBSCRIPTION_ID)" >> "$envFilePath"

# Confirm success
echo ".env file created successfully!"
