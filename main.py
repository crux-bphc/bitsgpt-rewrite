from src.agents import Agents

agents = Agents()

# print(agents.llm.invoke("What is the meaning of life?"))
print(agents.intent_classifier("What are some reviews for meow?", ""))