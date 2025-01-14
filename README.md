# o1 reasoning over machine learning models

This project leverages GPT-4 to extract features and their values from user input, which are then used as input for an ML model registered with MLflow. The extracted information is subsequently provided to a GPT o1 model to reason about the output, enabling advanced reasoning capabilities over the machine learning predictions.

By integrating GPT-4 and GPT o1, the project aims to enhance the interpretability and usability of machine learning models. The GPT-4 model processes user queries to identify and extract relevant features, which are then fed into the ML model. The results from the ML model are further analyzed by the GPT o1 model to provide comprehensive insights and reasoning, making the predictions more understandable and actionable for users.

This approach not only improves the accuracy of the predictions but also provides a deeper understanding of the underlying data and model behavior, facilitating better decision-making and more effective utilization of machine learning in various applications.

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


## Example of output by executing the main.py

Some loggings results


> 
INFO:azure.identity._credentials.environment:No environment configuration found.

INFO:root:
assistant: age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal
63,1,1,145,233,1,2,150,0,2.3,3,0,fixed
67,1,4,160,286,0,2,108,1,1.5,2,3,norma

INFO:root:Tests passed:
============================= test session starts =============================
platform win32 -- Python 3.12.8, pytest-8.3.4, pluggy-1.5.0
rootdir: C:\Users\karinaa\OneDrive - Microsoft\Documents\codes\azure-samples\gbbai-o1-reasoning-over-ml
plugins: anyio-4.8.0, Faker-33.3.0
collected 1 item

test\schema.py .                                                         [100%]

============================== 1 passed in 1.54s ==============================

INFO:root:Creating input data asset for model...
INFO:src.deploy_ml_model.create_input_data_for_model:Creating input data asset for model...

Uploading data (0.0 MBs): 100%|######################################################################| 154/154 [00:00<00:00, 1969.57it/s] 

INFO:root:Invoke endpoint...

Request method: 'GET'
Request headers:
    'Accept': 'application/json'
    'x-ms-client-request-id': '96e3d8ba-d11d-11ef-9fec-8c3b4a55ecfb'
    'User-Agent': 'azure-ai-ml/1.23.1 azsdk-python-mgmt-machinelearningservices/0.1.0 Python/3.12.8 (Windows-11-10.0.22631-SP0)'
    'Authorization': 'REDACTED'

INFO:root:Data asset path: 
INFO:azure.identity._internal.decorators:AzureCliCredential.get_token_info succeeded

INFO:root:Job name: batchjob-c4e096a3-198d-448c-a501-deca591c7130
INFO:root:Job status: Running. Waiting for 10 seconds before checking again...
INFO:root:Job status: Running. Waiting for 10 seconds before checking again...
INFO:root:Job status: Running. Waiting for 10 seconds before checking again...

────────────────────────────────────────────────────────────────────────────
1. Overview of the Predictions
────────────────────────────────────────────────────────────────────────────

• “prediction = 0” usually indicates the model predicts “no presence of heart disease.”
• “prediction = 1” usually indicates the model predicts “presence of heart disease.”

These predictions are based on the input features the model uses (age, sex, chest pain type, blood pressure, cholesterol, etc.). Each row in your list corresponds to a patient (or a single data point), the model’s decision (0 or 1), and the filename “heart-unlabeled-0.csv.”

For example, in your provided results:
• Row 0 has prediction 0.1 in your text, which might reflect either a probability or a slight formatting irregularity, but generally is associated with “no heart disease” (0).
• Row 1 has prediction 1 → “model suggests presence of heart disease.”
• Row 2 has prediction 0 → “model suggests no heart disease.”
• And so forth…

Most of the predictions here are 0, with a subset indicated as 1. That distribution can happen if the model sees fewer patients with strong risk factors or if the data share many characteristic patterns that align with “no presence of heart disease.”

────────────────────────────────────────────────────────────────────────────
2. Key Features Influencing Predictions
────────────────────────────────────────────────────────────────────────────

Even though we cannot see the exact features for each row, these are some of the important variables that typically influence a heart-disease classification model:

1) Chest Pain Type (cp):
   - Certain types of chest pain (like typical angina) more strongly correlate with heart disease.

2) Age:
   - As age increases, risk factors for heart disease can become more prominent.

3) Sex:
   - Sex can influence heart disease risk (e.g., in many datasets, male (1) has a slightly higher reported risk).

4) Blood Pressure (trestbps):
   - Higher resting blood pressure can be correlated with increased cardiovascular risk.

5) Cholesterol (chol):
   - Elevated cholesterol levels often factor into the likelihood the model assigns for heart disease.

6) Maximum Heart Rate (thalach):
   - Lower achievable heart rate can correlate with higher risk.

7) Exercise-Induced Angina (exang):
   - Angina (chest pain) triggered by exercise is a known risk indicator.

8) ST Depression (oldpeak) & Slope of the ST Segment (slope):
   - These ECG-related features often strongly correlate with heart conditions; a higher oldpeak or certain slopes tend to increase suspicion of heart disease.

9) Number of Major Vessels Colored (ca):
   - More vessels with issues can indicate higher risk.

10) Thalassemia (thal):
   - Certain results (like “fixed” or “reversible”) can point to underlying heart stress.

────────────────────────────────────────────────────────────────────────────
3. Why Rows Might Differ
────────────────────────────────────────────────────────────────────────────

• Each row represents a different patient or measurement set. Small differences in features (like whether chest pain is typical or atypical, how high the cholesterol is, or if someone experiences exercise-induced chest pain) can cause large changes in the model’s predicted probability.

• Because the model is trained to weigh all features together (e.g., possibly via a logistic regression, random forest, or similar supervised learning approach), it looks for patterns in the patient’s data that best match known cases with or without heart disease.

• A row receiving a “1” suggests that, upon examining these features, the model found it more likely than not that the patient’s data resemble past cases of heart disease.

• A row receiving a “0” suggests the model found that patient’s features more closely match individuals without heart disease.

────────────────────────────────────────────────────────────────────────────
4. Interpreting the Distribution of 0s and 1s
────────────────────────────────────────────────────────────────────────────

• High Frequency of Prediction “0”:
  If most of the rows have a predicted label “0,” the data for those specific patients likely resembled lower-risk patterns. Perhaps their test results (like chest pain type, cholesterol, blood pressure) did not align with the typical high-risk profiles learned by the model.

• Why Some Rows Are “1”:
  Where you see a “1,” the model likely identified risk factors or combinations of features frequently observed in individuals who do have heart disease. Examples might include older age, a higher cholesterol reading, presence of typical angina, certain ECG abnormalities, or other strong signals commonly associated with heart disease.

────────────────────────────────────────────────────────────────────────────
5. Limitations and Cautions
────────────────────────────────────────────────────────────────────────────

1) Model Limitations:
   - No model is perfect. It might produce false positives (predicting “1” when the individual does not have heart disease) or false negatives (predicting “0” when the individual does have heart disease).

2) Quality of the Data:
   - Predictions ultimately rely on the quality, completeness, and representativeness of the input features.

3) No Substitute for Medical Advice:
   - Even though the model is designed to help identify risk of heart disease, it cannot give a definitive conclusion about an individual’s health. A qualified medical professional should interpret the results and conduct further tests as necessary.

────────────────────────────────────────────────────────────────────────────
6. Summing Up
────────────────────────────────────────────────────────────────────────────

• Each row’s “0” or “1” classification is the model’s best guess about the presence of heart disease based on the patterns it has learned from historical data.
• A “1” typically flags potential concern, suggesting that the individual’s pattern of inputs (age, cholesterol, chest pain type, etc.) is consistent with heart-disease-positive cases seen during training.
• A “0” suggests the model did not detect strong patterns indicative of heart disease and found it more likely the individual was disease-free in similar cases from past data.

Overall, these predictions reflect how the ML model has interpreted the provided features. While the model’s probabilities may sometimes appear near a threshold (e.g., “0.1” or “0.9”), the final classification usually comes down to whether it crosses a specific decision boundary. Interpretation should therefore be combined with clinical judgment, additional diagnostics, and medical expertise.