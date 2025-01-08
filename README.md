# o1 reasoning over machine learning models

This project leverages GPT-4 to extract features and their values from user input, which are then used as input for an ML model registered with MLflow. The extracted information is subsequently provided to a GPT o1 model to reason about the output, enabling advanced reasoning capabilities over the machine learning predictions.

By integrating GPT-4 and GPT o1, the project aims to enhance the interpretability and usability of machine learning models. The GPT-4 model processes user queries to identify and extract relevant features, which are then fed into the ML model. The results from the ML model are further analyzed by the GPT o1 model to provide comprehensive insights and reasoning, making the predictions more understandable and actionable for users.

This approach not only improves the accuracy of the predictions but also provides a deeper understanding of the underlying data and model behavior, facilitating better decision-making and more effective utilization of machine learning in various applications.

## Prerequisites
+ [azd](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd), used to deploy all Azure resources and assets used in this sample.

+ [PowerShell Core pwsh](https://github.com/PowerShell/powershell/releases) if using Windows

+ Python 3.11

## Setup environment

This sample uses [`azd`](https://learn.microsoft.com/azure/developer/azure-developer-cli/) and a bicep template to deploy all Azure resources, including the Azure OpenAI models.

1. Login to your Azure account: `azd auth login`

2. Create an environment: `azd env new`

3. Run `azd up`.

   + Choose a name for your resourge group.
   + Enter a region for the resources.

   The deployment creates multiple Azure resources and runs multiple jobs. It takes several minutes to complete. The deployment is complete when you get a command line notification stating "SUCCESS: Your up workflow to provision and deploy to Azure completed."


## Features

This project framework provides the following features:

* Feature 1
* Feature 2
* ...

## Getting Started

### Setup

To setup the project, clone the repository and install the dependencies:

```bash
git https://github.com/Azure-Samples/gbbai-o1-reasoning-over-ml
cd gbbai-o1-reasoning-over-ml

python -m venv venv
source venv/bin/activate -> MAC
or
.\venv\Scripts\activate -> Windows

pip install -r requirements.txt
```

### ML Model Deployment

This script requires running the `deploy.sh` script located in the `deploy-ml-model` folder first.

```bash
cd deploy-ml-model
./deploy.sh
```

### Prerequisites

(ideally very short, if any)

- OS
- Library version
- ...

### Installation

(ideally very short)

- npm install [package name]
- mvn install
- ...

### Quickstart
(Add steps to get up and running quickly)

1. git clone [repository clone url]
2. cd [repository name]
3. ...


## Demo


To run the demo, follow these steps:

1. **Setup the infrastructure**: Prepare the necessary resources and environment.
2. **Deploy the model and the endpoint**: Follow the instructions to deploy the ML model and set up the endpoint.
3. **Ask the questions**: Interact with the deployed model by asking relevant questions.


The `main.py` script will proceed with the following steps:

1. **Ask a question**: The user inputs a question.

    ### Example question

    Q: dataset includes the following attributes: age (63), sex (1), cp (1), trestbps (145), chol (233), fbs (1), restecg (2), thalach (150), exang (0), oldpeak (2.3), slope (3), ca (0), and thal (fixed)

2. **Extract features and their values**: The script extracts relevant features and their values from the question.
3. **Save data as an asset**: The extracted data is saved as an asset in the ML workspace.


To access the ML model, you can visit the following link:

https://github.com/Azure/azureml-examples/tree/main/cli/endpoints/batch/deploy-models/heart-classifier-mlflow/deployment-simple

This link directs you to an example repository on GitHub provided by Azure. It contains instructions and code for deploying a heart classifier ML model using MLflow in a simple deployment setup. You can follow the steps in the repository to understand how to deploy and use the model.



## Resources

(Any additional resources or related projects)

- Link to supporting information
- Link to similar sample
- ...
