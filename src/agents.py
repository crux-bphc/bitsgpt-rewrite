import os
import textwrap

from dotenv import load_dotenv
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

from src.tools.memory_tool import tool_modify_memory

load_dotenv()


class Agents:
    def __init__(self):

        self.llm = ChatGroq(
            temperature=0,
            model="llama-3.3-70b-versatile",
        )
        print("Using GROQ API")

        self.prompts = {}

        prompts_directory = os.path.join(os.path.dirname(__file__), "./prompts")
        for agent_name in os.listdir(prompts_directory):
            with open(os.path.join(prompts_directory, agent_name)) as f:
                agent_name = agent_name.split(".")[0]
                self.prompts[agent_name] = f.read()

    def _get_prompt(
        self, agent_name: str, user_input: str, agent_scratchpad=False
    ) -> ChatPromptTemplate:

        prompt = [
            (
                "system",
                self.prompts[agent_name],
            ),
            (
                "user",
                textwrap.dedent(user_input),
            ),
        ]
        if agent_scratchpad:
            prompt.append(("placeholder", "{agent_scratchpad}"))
        return ChatPromptTemplate.from_messages(prompt)

    def intent_classifier(self, query: str, chat_history: str) -> str:
        prompt = self._get_prompt(
            "INTENT_CLASSIFIER_AGENT",
            f"<query>{query}</query>\n\n<history>{chat_history}</history>",
        )

        chain = prompt | self.llm

        result = chain.invoke(
            {
                "input": query,
            }
        )

        return result

    def general_campus_query(self, query: str, chat_history: str) -> str:
        prompt = self._get_prompt(
            "GENERAL_CAMPUS_QUERY_AGENT",
            f"<query>{query}</query>\n\n<history>{chat_history}</history>",
        )

        chain = prompt | self.llm

        result = chain.invoke(
            {
                "input": query,
            }
        )

        return result

    def course_query(self, query: str, chat_history: str) -> str:
        raise NotImplementedError("Course query not implemented yet")

    def long_term_memory(self, id: str, query: str, memories: str) -> str:
        tools = [tool_modify_memory]
        prompt = self._get_prompt(
            "LONG_TERM_MEMORY_AGENT", query, agent_scratchpad=True
        )
        agent = create_tool_calling_agent(self.llm, tools, prompt)
        chain = AgentExecutor(agent=agent, tools=tools)
        result = chain.invoke({"user_id": id, "memories": memories})
        return result["output"]
