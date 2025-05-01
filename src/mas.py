import os, asyncio
from jinja2 import Environment, FileSystemLoader
from azure.identity.aio import DefaultAzureCredential
from semantic_kernel.agents import AgentGroupChat, AzureAIAgent, AzureAIAgentSettings, ChatCompletionAgent
from semantic_kernel.agents.strategies import TerminationStrategy, SequentialSelectionStrategy
from semantic_kernel.contents import AuthorRole
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from agents.plugins.retrieval import RetrievalPlugin

class ApprovalTerminationStrategy(TerminationStrategy):
    """A strategy for determining when an agent should terminate."""

    async def should_agent_terminate(self, agent, history):
        """Check if the agent should terminate."""
        return "approved" in history[-1].content.lower()

# class for selection strategy
class SelectionStrategy(SequentialSelectionStrategy):
    """A strategy for determining which agent should take the next turn in the chat."""
    async def select_agent(self, agents, history):
        """Check which agent should take the next turn in the chat."""
        
        # If there is the command "/use_reasoning" in the chat history, select the Reasoning agent
        if "/use_reasoning" in history[-1].content:
            agent = next((agent for agent in agents if agent.name == "ReasoningAgent"), None)
        else:
            # Use the Analyst agent
            agent = next((agent for agent in agents if agent.name == "AnalystAgent"), None)        
        
        return agent


class Orchestrator:
    def __init__(self):
        self.ai_agent_settings = AzureAIAgentSettings()
        self.env = Environment(loader=FileSystemLoader(os.getenv('TEMPLATE_DIR_PROMPTS')))

        self.template_reasoning_agent = self.env.get_template(os.getenv('TEMPLATE_REASONING_AGENT'))
        self.template_analyst_agent = self.env.get_template(os.getenv('TEMPLATE_ANALYST_AGENT'))
        self.template_reviewer_agent = self.env.get_template(os.getenv('TEMPLATE_REVIEWER_AGENT'))
        self.template_orchestrator_agent = self.env.get_template(os.getenv('TEMPLATE_ORCHESTRATOR_AGENT'))

    # Clean all agents
    async def clean_agents(self):
        async with (DefaultAzureCredential() as creds,
                    AzureAIAgent.create_client(credential=creds) as client,
            ):
            existing_agents = await client.agents.list_agents()
            agents_to_delete = ["AnalystAgent", 
                                "ReviewerAgent"]

            for agent in existing_agents.data:                
                if agent.name in agents_to_delete:
                    print(f"Deleting agent: {agent.name}")
                    await client.agents.delete_agent(agent.id)

    async def get_or_create_azure_agent(self, client, existing_agents, name, description, instructions, plugins=[]):
        for agent in existing_agents.data:
            if agent.name == name:
                print(f"{name} already exists.")
                agent_definition = await client.agents.get_agent(agent.id)
                return AzureAIAgent(client=client, definition=agent_definition, plugins=plugins)

        agent_definition = await client.agents.create_agent(
            model=self.ai_agent_settings.model_deployment_name,
            name=name,
            temperature=0.0,
            description=description,
            instructions=instructions,

        )
        return AzureAIAgent(client=client, 
                            definition=agent_definition,
                            plugins=plugins)

    async def run(self, user_input):

        async with (DefaultAzureCredential() as creds,
                    AzureAIAgent.create_client(credential=creds,
                                               conn_str=self.ai_agent_settings.project_connection_string.get_secret_value()) as client,
            ):
            existing_agents = await client.agents.list_agents()

            reasoning_agent = ChatCompletionAgent(
                service=AzureChatCompletion(endpoint=self.ai_agent_settings.endpoint,
                                            deployment_name=self.ai_agent_settings.model_deployment_name,
                ),
                name="ReasoningAgent",
                instructions=self.template_reasoning_agent.render(),
                plugins=[RetrievalPlugin()],
            )

            analyst_agent = await self.get_or_create_azure_agent(
                client, existing_agents,
                name="AnalystAgent",
                description="Agent to analyze the reasoning based on shap values and provide insights",
                instructions=self.template_analyst_agent.render(),
            )

            agent_reviewer = await self.get_or_create_azure_agent(
                client, existing_agents,
                name="ReviewerAgent",
                description="Agent to review the responses",
                instructions=self.template_reviewer_agent.render(),
            )

            

            # Create the Agent Group
            agent_group = AgentGroupChat(
                agents=[reasoning_agent,
                        analyst_agent, 
                        agent_reviewer],
                termination_strategy=ApprovalTerminationStrategy(agents=[agent_reviewer],                                                                  
                                                                 maximum_iterations=3),
                selection_strategy=SelectionStrategy(),  
                )

            try:
                # Add the user_input as a message to the group chat
                await agent_group.add_chat_message(message=user_input)
                print(f"# {AuthorRole.USER}: '{user_input}'")

                # Invoke the chat
                async for content in agent_group.invoke():
                    print(f"# {content.role} - {content.name or '*'}: '{content.content}'")
            finally:
                # Cleanup: Delete the agents
                await agent_group.reset()
 
if __name__ == "__main__":
    orchestrator = Orchestrator()
    
    user_input = "Me ajude a interpretar os resultados do modelo de IA. /use_reasoning"

    # Clean all agents
    asyncio.run(orchestrator.clean_agents())

    # Run the agent group
    response = asyncio.run(orchestrator.run(user_input))
    
    # Print the response
    # print(response)
