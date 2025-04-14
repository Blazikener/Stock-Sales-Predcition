from gpt4all import GPT4All
from pathlib import Path
import pyttsx3
import speech_recognition as sr
import requests

model_path = Path(r"C:\Users\abdulahad\Desktop\HackEra\tinyllama-1.1b-chat-v1.0.Q2_K.gguf")
model = GPT4All(model_name=str(model_path), allow_download=False)

tts_engine = pyttsx3.init()
tts_engine.setProperty('rate', 175)
recognizer = sr.Recognizer()
mic = sr.Microphone()

API_URL = "http://127.0.0.1:8000"

context_memory = []  

def speak(text):
    print("Bot", text)
    tts_engine.say(text)
    tts_engine.runAndWait()

def listen():
    with mic as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            return recognizer.recognize_google(audio)
        except:
            return None

def update_context(user_input, response):
    context_memory.append(f"User: {user_input}")
    context_memory.append(f"Assistant: {response}")
    if len(context_memory) > 10:
        context_memory.pop(0)
        context_memory.pop(0)

def generate_context_prompt(current_input):
    history = "\n".join(context_memory)
    return f"{history}\nUser: {current_input}\nAssistant:"

def handle_command(prompt):
    if "predict sales" in prompt:
        data = {
            "TV": 1000.0, "Radio": 500.0, "Newspaper": 300.0,
            "Stock_Available": 40, "Stock_Used": 10,
            "Restock_Threshold": 5, "Reorder_Quantity": 20,
            "Stock_Replenished": 10, "Date": "2025-04-14"
        }
        res = requests.post(f"{API_URL}/predict", json=data)
        if res.ok:
            return f"Predicted sales are {res.json()['prediction']}"
        return "Failed to get prediction."

    elif "top selling" in prompt:
        res = requests.get(f"{API_URL}/top_selling")
        return res.json().get("message", "Couldn’t fetch data.")

    elif "stock alert" in prompt:
        res = requests.get(f"{API_URL}/stock_alerts")
        return res.json().get("message", "Couldn’t fetch stock alerts.")

    return None

with model.chat_session() as session:
    while True:
        try:
            prompt = listen()
            if not prompt:
                prompt = input("You (type): ")

            if prompt.lower() in ["exit", "quit", "stop"]:
                speak("Goodbye!")
                break

            command_response = handle_command(prompt)
            if command_response:
                response = command_response
            else:
                context_prompt = generate_context_prompt(prompt)
                response = session.generate(context_prompt)

            speak(response)
            update_context(prompt, response)

        except KeyboardInterrupt:
            print("Exiting...")
            break
