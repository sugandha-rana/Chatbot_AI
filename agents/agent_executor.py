# app/agents/agent_executor.py

from app.services.llm_service import LLMService
from app.agents.prompts import prompt_template
from app.agents.tools import tools_template

from langchain.agents import AgentExecutor, Tool
from langchain.agents.chat.base import ConversationalChatAgent


# 1. Map user type to prompt
USER_TYPE_PROMPTS = {
    "admin": prompt_template.admin_prompt,
    "responder": prompt_template.responder_prompt,
    "invittee": prompt_template.invittee_prompt,
}

# 2. Map user type to tools
USER_TYPE_TOOLS = {
    "admin": tools_template.admin_tools,
    "responder": tools_template.responder_tools,
    "invittee": tools_template.invittee_tools,
}


# 3. Getters
def get_prompt_for_user_type(user_type: str) -> str:
    return USER_TYPE_PROMPTS.get(user_type, "You are a helpful assistant.")


def get_tools_for_user_type(user_type: str) -> list[Tool]:
    return USER_TYPE_TOOLS.get(user_type, [])


# 4. AgentExecutorBuilder
class AgentExecutorBuilder:
    def __init__(self, user_type: str):
        self.prompt = get_prompt_for_user_type(user_type)
        self.tools = get_tools_for_user_type(user_type)
        self.llm = LLMService().model  # Gemini model

    def create(self) -> AgentExecutor:
        chat_agent = ConversationalChatAgent.from_llm_and_tools(
            llm=self.llm,
            tools=self.tools,
            system_message=self.prompt,
            verbose=True
        )

        return AgentExecutor.from_agent_and_tools(
            agent=chat_agent,
            tools=self.tools,
            verbose=True,
            handle_parsing_errors=True
        )
