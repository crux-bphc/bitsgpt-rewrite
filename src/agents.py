import os
import textwrap
from dotenv import load_dotenv


from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

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


    def get_prompt(self, agent_name: str, query: str, chat_history: str, agent_scratchpad=False) -> ChatPromptTemplate:

        prompt = [
            (
                "system",
                self.prompts[agent_name],
            ),
            (
                "user",
                textwrap.dedent(f"<query>{query}</query>\n\n<history>{chat_history}</history>"),
            ),
        ]
        if agent_scratchpad:
            prompt.append(("placeholder", "{agent_scratchpad}"))
        return ChatPromptTemplate.from_messages(prompt)
    
    def intent_classifier(self, query: str, chat_history: str) -> str:
        prompt = self.get_prompt("INTENT_CLASSIFIER_AGENT", query, chat_history)

        chain = prompt | self.llm

        result = chain.invoke({
            "input": query,
        })

        return result.content

    def general_campus_query(self, query: str, chat_history: str) -> str:
        prompt = self.get_prompt("GENERAL_CAMPUS_QUERY_AGENT", query, chat_history)

        chain = prompt | self.llm

        result = chain.invoke({
            "input": query,
        })

        return result.content