from agents.prompts.prompts import get_prompt_for_role
from agents.tools import get_tools_for_role
from service.llm_service import LLMService
from langchain.agents import AgentExecutor, Tool
from langchain.agents import ConversationalChatAgent
from typing import List

llm_service = LLMService()

class AgentExecutorBuilder:
    def __init__(self, user_type: str) -> None:
        """
        Initialize the AgentExecutorBuilder with user_type.

        Args:
            user_type (str): The user type/role to get tools and prompt for.
        """
        print(f"Initializing AgentExecutorBuilder for user_type: {user_type}")
        self.llm = llm_service.model
        self.tools = get_tools_for_role(user_type)
        print(f"Tools loaded: {[tool.name for tool in self.tools]}")
        self.system_prompt = get_prompt_for_role(user_type)
        print(f"System prompt set: {self.system_prompt[:100]}...")

    def create(self) -> AgentExecutor:
        """
        Create and return an AgentExecutor instance using the ConversationalChatAgent.

        Returns:
            AgentExecutor: Configured agent executor instance.
        """
        print("Creating ConversationalChatAgent with provided LLM, tools, and system prompt.")
        chat_agent = ConversationalChatAgent.from_llm_and_tools(
            llm=self.llm,
            tools=self.tools,
            system_message=self.system_prompt,
            verbose=True
        )
        print("ConversationalChatAgent created successfully.")

        agent_executor = AgentExecutor.from_agent_and_tools(
            agent=chat_agent,
            tools=self.tools,
            verbose=True,
            handle_parsing_errors=True
        )
        print("AgentExecutor instance created successfully.")
        return agent_executor
