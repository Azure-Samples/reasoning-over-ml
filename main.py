import os
import logging
from openai import AzureOpenAI
from dotenv import load_dotenv
from src.assistant import AIAssistant
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

from azure.ai.inference.prompts import PromptTemplate
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from jinja2 import Environment, FileSystemLoader

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.getLogger("azure.identity").setLevel(logging.WARNING)


# Load environment variables from a .env file
load_dotenv()


# Load environment variables from a .env file
load_dotenv(override=True)

class MLAssistant:
    def __init__(self, instructions_file_name, use_o1=False, tools=None, functions=None):
        self.use_o1 = use_o1
        self.client = self.create_client()
        self.instructions_file_name = instructions_file_name
        self.instructions = self.load_instructions()
        self.model = os.getenv("AZURE_OPENAI_MODEL_NAME")
        self.assistant = self.create_assistant()
        

    def create_client(self):
        if self.use_o1:
            return AzureOpenAI(
                api_key=os.getenv("AZURE_OPENAI_KEY_O1"),
                api_version=os.getenv("AZURE_OPENAI_API_VERSION_O1"),
                azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT_O1"),
            )
        else:
            return AzureOpenAI(
                api_key=os.getenv("AZURE_OPENAI_KEY"),
                api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
                azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
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
        return self.assistant.chat()


class o1Chat():

    def get_chat_response(self, messages, context, prompt_template):
        
        client = AzureOpenAI(
        azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT_O1"), 
        api_key=os.getenv("AZURE_OPENAI_API_KEY_O1"),  
        api_version=os.getenv("AZURE_OPENAI_API_VERSION_O1")
        )

        # generate system message from the template, passing in the context as variables
        system_message = prompt_template.create_messages(data=context) 

        system_message[0]["role"] = "assistant"

        response = client.chat.completions.create(
            model=os.getenv("AZURE_OPENAI_MODEL_NAME_O1"),
            messages=system_message + messages,
            max_completion_tokens=5000
        )
        return response

    def get_prompt_template_from_jinja2(
        self,
        prompt_path: str,
        prompt_name: str,
        jinja2_placeholders: dict[str, str]={},
        ) -> PromptTemplate:
        """
        Loads a .txt file as a Jinja2 template and converts it into a LangChain PromptTemplate.

        Parameters:
                prompt_path: Path to the prompt.
                prompt_name: Filename of the prompt, including its extension.
                jinja2_placeholders: A dictionary of placeholders to be replaced in the Jinja2 template.
        """

        env = Environment(loader=FileSystemLoader(prompt_path))
        template = env.get_template(prompt_name)
        prompt_string = template.render(jinja2_placeholders)

        # create a prompt template from an inline string (using mustache syntax)
        prompt_template = PromptTemplate.from_string(
            prompt_string
        )
        return prompt_template
    

class o1ChatFoundry(o1Chat):
    def __init__(self):
        super().__init__()
        project_connection_string = os.getenv("CONNSTRING")

        project = AIProjectClient.from_connection_string(
            conn_str=project_connection_string, credential=DefaultAzureCredential()
        )

        self.chat = project.inference.get_chat_completions_client()


    def get_chat_response(self, messages, context, prompt_template):

        # generate system message from the template, passing in the context as variables
        system_message = prompt_template.create_messages(data=context)

        # add the prompt messages to the user messages
        response = self.chat.complete(
            model=os.getenv("AZURE_OPENAI_MODEL_NAME_O1"),
            messages=system_message + messages,
            temperature=1,
            frequency_penalty=0.5,
            presence_penalty=0.5,
        )

        return response

# Create a method to initialize the assistant
def initialize_assistant():
    instructions_file = "../src/instructions/instructions-features-info.jinja2"
    return MLAssistant(instructions_file)


# Main function
if __name__ == "__main__":

    #TODO Input as csv
    #TODO: Code interpreter - Shap Values
    assistant = initialize_assistant()
    score = assistant.chat()
    score = score.to_string(index=False)

    print(score)

    o1 = o1Chat()
    prompt_template = o1.get_prompt_template_from_jinja2("/src/instructions/", "instructions-model-output.jinja2")
    response = o1.get_chat_response(
    messages=[{"role": "user", "content": f"please, give me a detailed and great explanation about the ACTUAL predictions: {score}"}],
    context={""},
    prompt_template=prompt_template
    )
    print(response.choices[0].message.content)

# Example question: age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal 63,1,1,145,233,1,2,150,0,2.3,3,0,fixed; 67,1,4,160,286,0,2,108,1,1.5,2,3,normal"
