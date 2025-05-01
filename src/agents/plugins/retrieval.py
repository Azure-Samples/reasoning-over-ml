import os
from semantic_kernel.functions import kernel_function
import csv


class RetrievalPlugin:
    """A plugin for retrieving documents from local."""
    def __init__(self):
        self.file_path = os.getenv('SHAP_DATASET_FILE_PATH')

    @kernel_function(name="RawShapValues",
                     description="Retrieve the raw shap-values from a file.")
    async def retrieve_shap_values(self) -> dict:
        """Retrieve shap values."""
        # Get the file path from the environment variable
        if not self.file_path:
            raise ValueError("File path is not set in the environment variables.")
        
        # Read the CSV file and return its content as a list of dictionaries

        with open(self.file_path, 'r') as file:
            reader = csv.DictReader(file)
            content = [row for row in reader]
        
        return {"raw-shap-dataset": content}