import os
import pickle
import pandas as pd


def init():
    global model
    global dtypes
    global explainer
    global columns
    
    # Get the model path from the environment variable
    root_path = os.path.join(os.environ["AZUREML_MODEL_DIR"], "model_artifacts")
    model_path = os.path.join(root_path,  "model.pkl")

    # Load the model
    with open(model_path, 'rb') as f:
        model = pickle.load(f)

    # Load the dtypes
    dtypes_path = os.path.join(root_path, 'X_test.pkl')    
    with open(dtypes_path, 'rb') as f:
        dataset = pickle.load(f)
        dtypes = dataset.dtypes.to_dict()
    
    # Load the columns
    columns = dataset.columns.tolist()
    
    # Load the shap explainer
    explainer_path = os.path.join(root_path, 'explainer.pkl')
    with open(explainer_path, 'rb') as f:
        explainer = pickle.load(f)
    
    print('Model, dtypes and explainer loaded successfully')
   

def run(mini_batch) -> pd.DataFrame:
    results_predictions = []
    results_shap_values = []

    print('Running the model')
    # Make predictions using the loaded model
    try:    
        data = pd.read_csv(mini_batch[0])
        data = data.astype(dtypes)

        # Predict using the loaded model
        predictions = model.predict(data)
        results_predictions.append(predictions.tolist())

        # Get the SHAP values
        shap_values = explainer.shap_values(data)
        results_shap_values.append(shap_values.tolist())
        
    except Exception as e:
        print(e)
        return str(e)
    
    # Combine the results into a single DataFrame
    results = pd.DataFrame(shap_values, columns=columns)
    results['prediction'] = predictions

    
    return results
