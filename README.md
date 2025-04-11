# <img src="./docs/img/azure_logo.png" alt="Azure Logo" style="width:30px;height:30px;"/> AOAI Reasoning Models over Machine Learning Custom Models

This project harnesses the power of AOAI to extract key features and their corresponding values from user input, which are then passed to an ML model managed via MLflow. The output from the ML model is subsequently fed into a reasoning model, enabling advanced interpretation and analysis of the predictions.

By integrating GPT-4 (or GPT-4o) with dedicated reasoning models, the project enhances the interpretability and practical utility of machine learning outcomes. GPT-4 processes user queries to identify and extract pertinent features that guide the ML model in generating predictions, after which the reasoning model scrutinizes these predictions to offer detailed insights, making the results more understandable and actionable.

This repository also facilitates batch endpoint calls within the assistant. By deploying an MLflow model from the deploy-ml-model folder, users can seamlessly integrate batch endpoint results with the reasoning model, enabling automated and scalable workflows.

## Key Features Overview

This project is designed to seamlessly enhance your machine learning workflows with cutting-edge capabilities that combine feature extraction, model integration, and advanced feature engineering.

### 1. Advanced Feature Extraction
- Leverages GPT-4 to automatically identify and extract relevant features and corresponding values from user input.
- Ensures that the data fed into the ML model is both precise and meaningful.

### 2. ML Model Integration
- Integrates with MLflow to utilize pre-registered machine learning models for generating accurate predictions.
- Detailed guidance is available for creating and configuring MLflow model artifacts, including best practices for endpoint batch deployments.

### 3. Effective Model Deployment
- Provides instructions for deploying the ML model so the assistant can explain predictions effectively after endpoint calls.
- For step-by-step guidance on deploying the ML model and setting up the endpoint, please refer to the [deploy_ml_model Readme](train/README.md). This document offers detailed instructions on configuring your environment, deploying the model, and verifying the deployment.

### 4. Enhanced Feature Engineering
- **Feature Identification:** Automatically recognizes and extracts key features from raw data inputs.
- **Data Refinement:** Suggests optimal transformations and engineering techniques aligned with model requirements.
- **Seamless Pipeline Integration:** Incorporates engineered features into the model training and evaluation workflow, boosting overall predictive performance.

*Note: Some functionalities, especially within feature engineering, are under active development. Stay tuned for continuous updates and improvements!*

### 5. **Streamlit Interface** (To Be Implemented)

*Note: Some functionalities, especially within feature engineering, are under active development. Stay tuned for continuous updates and improvements!*

TODO:

- Implement a parser for when the user provides just an Excel file with features.
- Implement a method that sends the outputs directly to O1, in case the user already has the outputs and does not wish to execute the batch endpoint.
- Implement the Streamlit interface.

## Getting Started

### Prerequisites

- Ensure you have an active Azure subscription.
- [azd](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd), used to deploy all Azure resources and assets used in this sample.
- [PowerShell Core pwsh](https://github.com/PowerShell/powershell/releases) if using Windows.
- Python 3.11.
- Confirm that you have the required ML libraries installed.

### Setup

To set up the project, clone the repository and install the dependencies:

```bash
git clone https://github.com/Azure-Samples/reasoning-over-ml
cd gbbai-o1-reasoning-over-ml

python -m venv venv
# For macOS:
source venv/bin/activate
# For Windows:
.\venv\Scripts\activate

pip install -r requirements.txt
```

### Setup Environment

This sample uses [`azd`](https://learn.microsoft.com/azure/developer/azure-developer-cli/) and a bicep template to deploy all Azure resources, including the Azure OpenAI models.

1. Login to your Azure account:
   `azd auth login`

2. Create an environment:
   `azd env new`

3. Run `azd up`:
   - Choose a name for your resource group.
   - Enter a region for the resources.

   The deployment creates multiple Azure resources and runs several jobs. It may take several minutes to complete. The deployment is complete when you receive a command line notification stating "SUCCESS: Your up workflow to provision and deploy to Azure completed."

## Demo

To run the demo, follow these steps:

1. **Setup the Infrastructure:** Prepare the necessary resources and environment.
2. **Deploy the Model and Endpoint:** Follow the instructions to deploy the ML model and set up the endpoint.
3. **Ask the Questions:** Interact with the deployed model by asking relevant questions.

The `main.py` script proceeds with the following steps:

1. **Ask a Question:** The user inputs a question.

   ### Example Question

   Q: dataset includes the following attributes: age (63), sex (1), cp (1), trestbps (145), chol (233), fbs (1), restecg (2), thalach (150), exang (0), oldpeak (2.3), slope (3), ca (0), and thal (fixed)

2. **Extract Features and Their Values:** The script extracts relevant features and their values from the question.
3. **Save Data as an Asset:** The extracted data is saved as an asset in the ML workspace.

## Example Output from main.py and Using O1 to Explain ML Predictions

Logging Results:

> INFO:azure.identity._credentials.environment:No environment configuration found.
>
> INFO:root:
> assistant: age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal
> 63,1,1,145,233,1,2,150,0,2.3,3,0,fixed
> 67,1,4,160,286,0,2,108,1,1.5,2,3,norma
>
> INFO:root:Tests passed:
> ============================= test session starts =============================
> platform win32 -- Python 3.12.8, pytest-8.3.4, pluggy-1.5.0
> plugins: anyio-4.8.0, Faker-33.3.0
> collected 1 item
>
> test\schema.py .                                                         [100%]
>
> ============================== 1 passed in 1.54s ==============================
>
> INFO:root:Creating input data asset for model...
> INFO:src.deploy_ml_model.create_input_data_for_model:Creating input data asset for model...
>
> Uploading data (0.0 MBs): 100%|######################################################################| 154/154 [00:00<00:00, 1969.57it/s]
>
> INFO:root:Invoke endpoint...
>
> Request method: 'GET'
> Request headers:
>     'Accept': 'application/json'
>     'User-Agent': 'azure-ai-ml/1.23.1 azsdk-python-mgmt-machinelearningservices/0.1.0 Python/3.12.8 (Windows-11-10.0.22631-SP0)'
>     'Authorization': 'REDACTED'
>
> INFO:root:Data asset path:
> INFO:azure.identity._internal.decorators:AzureCliCredential.get_token_info succeeded
>
> INFO:root:Job name: batchjob-c4e096a3-198d-448c-a501-deca591c7130
> INFO:root:Job status: Running. Waiting for 10 seconds before checking again...
> INFO:root:Job status: Running. Waiting for 10 seconds before checking again...
> INFO:root:Job status: Running. Waiting for 10 seconds before checking again...

---
1. Overview of the Predictions
---

• “prediction = 0” usually indicates the model predicts “no presence of heart disease.”
• “prediction = 1” usually indicates the model predicts “presence of heart disease.”

These predictions are based on the input features used by the model (age, sex, chest pain type, blood pressure, cholesterol, etc.). Each row corresponds to a patient (or a single data point), the model’s decision (0 or 1), and a filename like “heart-unlabeled-0.csv.”

For example, in the provided results:
• Row 0 shows a prediction of 0.1, which might reflect a probability or slight formatting irregularity, but generally is associated with “no heart disease” (0).
• Row 1 shows a prediction of 1, indicating the model suggests the presence of heart disease.
• Row 2 shows a prediction of 0, suggesting the model indicates no heart disease.

Most predictions are 0, with a few indicated as 1. This pattern can occur if the model sees fewer patients with strong risk factors or if the data resemble lower-risk profiles overall.

---
2. Key Features Influencing Predictions
---

Even though exact features per row are not displayed, key variables typically influencing a heart-disease classification model include:

1) Chest Pain Type (cp):
   - Certain types, such as typical angina, strongly correlate with heart disease.

2) Age:
   - Increased age can heighten the risk factors for heart disease.

3) Sex:
   - Risk factors may vary by sex; in many datasets, male (1) may have a slightly higher risk.

4) Blood Pressure (trestbps):
   - Higher resting blood pressure can correlate with increased cardiovascular risk.

5) Cholesterol (chol):
   - Elevated cholesterol often factors into the model’s prediction for heart disease.

6) Maximum Heart Rate (thalach):
   - Lower maximum heart rate can be associated with higher risk.

7) Exercise-Induced Angina (exang):
   - Chest pain triggered by exercise is a known risk indicator.

8) ST Depression (oldpeak) & Slope of the ST Segment (slope):
   - Certain ECG features can indicate higher risk for heart conditions.

9) Number of Major Vessels Colored (ca):
   - A higher count may indicate elevated risk.

10) Thalassemia (thal):
   - Values like “fixed” or “reversible” can indicate underlying cardiac stress.

---
3. Why Rows Might Differ
---

• Each row represents a different patient or measurement set. Small differences in features, like variations in chest pain type or cholesterol levels, can lead to different predictions.
• The model weighs all features—using methods such as logistic regression or random forest—to match input patterns with historical data.
• A row with a prediction of “1” suggests that the patient’s data resemble cases of heart disease, whereas a “0” suggests a closer match to patients without heart disease.

---
4. Interpreting the Distribution of 0s and 1s
---

• High Frequency of Prediction “0”: 
  Indicates that most patients have data that align with lower risk.
  
• Occurrence of Prediction “1”: 
  Highlights patients whose features strongly match historical patterns of heart disease.

---
5. Limitations and Cautions
---

1) Model Limitations:
   - No model is infallible; false positives and negatives can occur.
2) Data Quality:
   - The accuracy of predictions relies on the quality, completeness, and representativeness of the input features.
3) Not a Substitute for Medical Advice:
   - The model’s output is not a definitive diagnosis. Always consult a qualified medical professional for proper evaluation and diagnosis.

---
6. Summing Up
---

• Each row’s classification (0 or 1) reflects the model’s best guess about the presence of heart disease.
• A prediction of “1” flags potential concern by identifying high-risk input patterns, while “0” suggests the opposite.
• Interpretation should combine model insights with clinical judgment and further diagnostics.

## Resources

- [Azure OpenAI Documentation](https://learn.microsoft.com/azure/cognitive-services/openai/)
- Additional links and references as required.
