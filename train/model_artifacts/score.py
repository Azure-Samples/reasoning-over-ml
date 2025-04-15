import os, json
import pickle
import pandas as pd
from typing import List


def init():
    global model
    
    os.environ["AZUREML_MODEL_DIR"] = '/home/azureuser/cloudfiles/code/Users/lubraz/reasoning-over-ml/train/artifacts/'

    # Get the model path from the environment variable
    model_path = os.environ["AZUREML_MODEL_DIR"]
    model_path = os.path.join(model_path, "model.pkl")

    # Load the model
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    
    print('Model loaded successfully', model)
   

def run(mini_batch) -> pd.DataFrame:
    results = []

    print('Running the model')
    print('Mini batch:', mini_batch)
    # Make predictions using the loaded model
    try:
        for record in mini_batch:
            print('Record:', record)
            data = pd.DataFrame(record['minibatch'])
            
            # For each data row make a prediction
            for index, row in data.iterrows():
                print('Processing row:', index)
                predictions = model.predict(row)           
                results.append(predictions.tolist())
    except Exception as e:
        print(e)
        return str(e)
    
    return pd.DataFrame(results)

if __name__ == "__main__":
    init()
    run([{"id": 0, 
         "dequeue_count": 3, 
         "minibatch": ["/home/azureuser/cloudfiles/code/Users/lubraz/reasoning-over-ml/train/artifacts/X_test.csv"], 
         "task_type": 4, 
         "input_start_time": 1744658925.750685, 
         "input_duration": 9.5367431640625e-07}])