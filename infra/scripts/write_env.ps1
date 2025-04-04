$envFilePath="../../.env"

If (Test-Path $envFilePath) {
    Remove-Item $envFilePath -Force
}
New-Item -Path $envFilePath -ItemType File -Force | Out-Null

# Add comments to the .env file
Add-Content -Path $envFilePath -Value "# Please do not share this file, or commit this file to the repository"
Add-Content -Path $envFilePath -Value "# This file is used to store the environment variables for the project for demos and testing only"
Add-Content -Path $envFilePath -Value "# Delete this file when done with demos, or if you are not using it"


Add-Content -Path $envFilePath -Value ("LOCATION=" + (azd env get-value AZURE_LOCATION))
Add-Content -Path $envFilePath -Value ("RESOURCE_GROUP=" + (azd env get-value RESOURCE_GROUP))
Add-Content -Path $envFilePath -Value ("AZURE_OPENAI_MODEL_NAME=" + (azd env get-value AZURE_OPENAI_MODEL_NAME))
Add-Content -Path $envFilePath -Value ("AZURE_OPENAI_API_VERSION=" + (azd env get-value AZURE_OPENAI_API_VERSION))
Add-Content -Path $envFilePath -Value ("AZURE_OPENAI_ENDPOINT=" + (azd env get-value AZURE_OPENAI_ENDPOINT))
Add-Content -Path $envFilePath -Value ("SUBSCRIPTION_ID=" + (azd env get-value SUBSCRIPTION_ID))

