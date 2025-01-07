import os
import logging
from openai import AzureOpenAI
import argparse
from dotenv import load_dotenv
from src.assistant import AIAssistant

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Load environment variables from a .env file
load_dotenv()


class MLAssistant:
    def __init__(self, instructions_file_name, tools=None, functions=None):
        self.client = self.create_client()
        self.instructions_file_name = instructions_file_name
        self.instructions = self.load_instructions()
        self.model = os.getenv("AZURE_OPENAI_MODEL_NAME")
        self.assistant = self.create_assistant()

    def create_client(self):
        return AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_KEY"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        )

    def load_instructions(self):
        instructions_path = os.path.join(
            os.path.dirname(__file__), "instructions", self.instructions_file_name
        )
        with open(instructions_path) as file:
            return file.read()

    def create_assistant(self):
        return AIAssistant(
            client=self.client,
            verbose=True,
            name="AI Assistant",
            instructions=self.instructions,
            model=self.model,
        )

    def chat(self):
        self.assistant.chat()


# Create a method to initialize the assistant
def initialize_assistant():
    instructions_file = "../src/instructions/instructions-features-info.jinja2"
    return MLAssistant(instructions_file)


# Main function
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ML with O1 Reasoning Assistant")
    # parser.add_argument()
    args = parser.parse_args()
    ml_assistant = initialize_assistant()
    ml_assistant.chat()
