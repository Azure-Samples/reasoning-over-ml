param location string 
param name string

resource runPowerShellInlineWithOutput 'Microsoft.Resources/deploymentScripts@2020-10-01' = {
  name: 'runPowerShellInlineWithOutput'
  location: location
  kind: 'AzurePowerShell'
  properties: {
    azPowerShellVersion: '8.3'
    scriptContent: '''
    If (Test-Path ../../.env) {
        Remove-Item ../../.env -Force
    }
    New-Item -Path ../../.env -ItemType File -Force | Out-Null
    Add-Content -Path ../../.env -Value ("AZURE_LOCATION=" + (azd env get-value AZURE_LOCATION))
    Add-Content -Path ../../.env -Value ("RESOURCE_GROUP=" + (azd env get-value RESOURCE_GROUP))
    Add-Content -Path ../../.env -Value ("AZURE_OPENAI_MODEL_NAME=" + (azd env get-value AZURE_OPENAI_MODEL_NAME))
    Add-Content -Path ../../.env -Value ("AZURE_OPENAI_API_VERSION=" + (azd env get-value AZURE_OPENAI_API_VERSION))
    Add-Content -Path ../../.env -Value ("AZURE_OPENAI_ENDPOINT=" + (azd env get-value AZURE_OPENAI_ENDPOINT))
    '''
    arguments: '-name ${name}'
    timeout: 'PT1H'
    cleanupPreference: 'OnSuccess'
    retentionInterval: 'P1D'
  }
}
