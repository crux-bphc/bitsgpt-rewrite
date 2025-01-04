from src.app import BitsGPT

bitsgpt = BitsGPT()

state = {
    "messages": ["What is the capital of France?"],
    "chat_history": ""
}
print(bitsgpt.app.invoke(state))