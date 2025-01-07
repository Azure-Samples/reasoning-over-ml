from openai import AzureOpenAI
import openai
from openai.types.beta import Thread
from openai.types.beta.threads import Run, Message
import time
import csv


class AIAssistant:
    def __init__(
        self,
        client: AzureOpenAI,
        verbose: bool = True,
        name: str = "AI Assistant",
        description: str = "An AI Assistant",
        instructions: str = None,
        model: str = None,
        auto_delete: bool = True,
    ):
        self.client = client
        self.verbose = verbose
        self.threads = []
        self.functions = []
        self.name = name
        self.description = description
        self.instructions = instructions
        self.model = model
        self.auto_delete = auto_delete

        try:
            self.assistant = self.client.beta.assistants.create(
            name=self.name,
            description=self.description,
            instructions=self.instructions,
            model=self.model,
        )
            
            self.assistant_id = self.assistant.id

        except openai.BadRequestError as e:
            print(f"Error details: {e}")
            print(f"Request data: {e.param}")


        

    def create_thread(self) -> Thread:
        thread = self.client.beta.threads.create()
        self.threads.append(thread)
        return thread



    def create_file(self, filename: str, file_id: str):
        content = self.client.files.retrieve_content(file_id)
        with open(filename.split("/")[-1], "w") as file:
            file.write(content)

    def format_message(self, message: Message) -> str:
        if getattr(message.content[0], "text", None) is not None:
            message_content = message.content[0].text
        else:
            message_content = message.content[0]
        annotations = message_content.annotations
        citations = []
        for index, annotation in enumerate(annotations):
            message_content.value = message_content.value.replace(
                annotation.text, f" [{index}]"
            )
            if file_citation := getattr(annotation, "file_citation", None):
                cited_file = self.client.files.retrieve(file_citation.file_id)
                citations.append(
                    f"[{index}] {file_citation.quote} from {cited_file.filename}"
                )
            elif file_path := getattr(annotation, "file_path", None):
                cited_file = self.client.files.retrieve(file_path.file_id)
                citations.append(f"[{index}] file: {cited_file.filename} is downloaded")
                self.create_file(filename=cited_file.filename, file_id=cited_file.id)

        message_content.value += "\n" + "\n".join(citations)
        return message_content.value

    def extract_run_message(
        self, run: Run, thread_id: str, output_role: bool = True
    ) -> str:
        messages = self.client.beta.threads.messages.list(
            thread_id=thread_id,
        ).data
        for message in messages:
            if message.run_id == run.id:
                return (
                    f"{message.role}: " + self.format_message(message=message)
                    if output_role
                    else self.format_message(message=message)
                )
        return "Assistant: No message found"


    def create_response(
        self,
        question: str,
        thread_id: str = None,
        run_instructions: str = None,
        max_retries: int = 5,
        retry_delay: int = 20,
    ) -> str:

        if thread_id is None:
            thread = self.create_thread()
            thread_id = thread.id

        self.client.beta.threads.messages.create(
            thread_id=thread_id, role="user", content=question
        )

        retries = 0

        while retries < max_retries:
            run = self.client.beta.threads.runs.create(
                thread_id=thread_id,
                assistant_id=self.assistant.id,
                instructions=run_instructions,
            )
            arguments = []

            while run.status not in ["completed", "failed"]:
                run = self.client.beta.threads.runs.retrieve(
                    thread_id=thread_id, run_id=run.id
                )
                if run.status == "expired":
                    raise Exception(
                        f"Run expired when calling {self.get_required_functions_names(run=run)}"
                    )
                time.sleep(0.5)

            if run.status == "failed":
                retries += 1
                print(
                    f"Run failed with the message: {run.last_error.message} \
                      Retrying in {retry_delay} seconds... (Attempt {retries}/{max_retries})"
                )
                time.sleep(retry_delay)
            else:
                tokens = {
                    "prompt_tokens": run.usage.prompt_tokens,
                    "completion_tokens": run.usage.completion_tokens,
                }
                return {
                    "answer": "\n"
                    + self.extract_run_message(run=run, thread_id=thread_id),
                    "total_tokens": tokens,
                }

    def chat(self, file_ids: list[str] = None):
        thread = self.create_thread()
        user_input = ""
        while user_input != "bye" and user_input != "exit":
            user_input = input("\033[32m Please, input your ask (or bye to exit) : ")
            response = self.create_response(question=user_input, thread_id=thread.id)
            message = response["answer"]

            # Extract feature names and values from the message
            lines = message.replace('assistant: ', '').split('\n')
            feature_names = []
            values = []
            for line in lines:
                if line.startswith('Feature Names: '):
                    feature_names = line.replace('Feature Names: ', '').split(', ')
                elif line.startswith('Values: '):
                    values = line.replace('Values: ', '').split(', ')

            # Write to a CSV file
            with open('src/ml-prediction/output.csv', 'w', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(feature_names)
                csvwriter.writerow(values)

            tokens = response["total_tokens"]
            print(f"\033[33m{message}")
            print(f"\033[33m{tokens}")

        if self.auto_delete:
            if file_ids:
                for file in file_ids:
                    self.delete_file(file_id=file)
            self.client.beta.threads.delete(thread_id=thread.id)
            self.client.beta.assistants.delete(assistant_id=self.assistant.id)

    def create_message(self, thread_id: str, role: str, question: str):
        self.client.beta.threads.messages.create(
            thread_id=thread_id, role="user", content=question
        )

    def create_response_with_handler(
        self,
        question: str,
        thread_id: str = None,
        run_instructions: str = None,
        max_retries: int = 5,
        retry_delay: int = 20,
        verbose: bool = True,
    ) -> str:
        if thread_id is None:
            thread = self.create_thread()
            thread_id = thread.id

        self.client.beta.threads.messages.create(
            thread_id=thread_id, role="user", content=question
        )

        retries = 0

        while retries < max_retries:
            run = self.client.beta.threads.runs.create(
                thread_id=thread_id,
                assistant_id=self.assistant.id,
                instructions=run_instructions,
            )
            arguments = []

            while run.status not in ["completed", "failed"]:
                run = self.client.beta.threads.runs.retrieve(
                    thread_id=thread_id, run_id=run.id
                )
                if run.status == "expired":
                    raise Exception(
                        f"Run expired when calling {self.get_required_functions_names(run=run)}"
                    )

                time.sleep(0.5)

            if run.status == "failed":
                retries += 1
                print(
                    f"Run failed. Retrying in {retry_delay} seconds... (Attempt {retries}/{max_retries})"
                )
                time.sleep(retry_delay)
            else:
                tokens = {
                    "prompt_tokens": run.usage.prompt_tokens,
                    "completion_tokens": run.usage.completion_tokens,
                }

                return
