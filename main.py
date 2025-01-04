from src.app import BitsGPT

bitsgpt = BitsGPT()

state = {
    "messages": ["I want to know about the fests"],
    "chat_history": ""
}
print(bitsgpt.app.invoke(state))