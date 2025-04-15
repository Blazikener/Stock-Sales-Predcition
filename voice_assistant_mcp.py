from gpt4all import GPT4All
from pathlib import Path
import pyttsx3
import speech_recognition as sr
import requests
import pandas as pd
from datetime import datetime, timedelta

#Save the llm model in the same location as your other files
model_path = Path(r"tinyllama-1.1b-chat-v1.0.Q2_K.gguf")
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

#Update context for mcp to understand
def update_context(user_input, response):
    context_memory.append(f"User: {user_input}")
    context_memory.append(f"Assistant: {response}")
    if len(context_memory) > 10:
        context_memory.pop(0)
        context_memory.pop(0)

def generate_context_prompt(current_input):
    history = "\n".join(context_memory)
    return f"{history}\nUser: {current_input}\nAssistant:"

CSV_PATH = "Advertising_Extended.csv"

def handle_command(prompt):
    try:
        df = pd.read_csv(CSV_PATH)

        # Convert Date column to datetime
        df['Date'] = pd.to_datetime(df['Date'])

        prompt = prompt.lower()

        # Predict sales using a simple formula or the latest row
        if "predict sales" in prompt:
            latest = df.iloc[-1]
            sales_prediction = latest["TV"] * 0.045 + latest["Radio"] * 0.04 + latest["Newspaper"] * 0.02
            return f"Predicted sales based on recent inputs: {sales_prediction:.2f} units."

        # Stock alerts for low inventory
        elif "stock alert" in prompt or "low stock" in prompt:
            low_stock_df = df[df["Stock_Available"] <= df["Restock_Threshold"]]
            if low_stock_df.empty:
                return "All items are well stocked."
            return f"{len(low_stock_df)} item(s) need restocking based on current data."

        # Top-selling entries in the past 7 days
        elif "top selling" in prompt or "top sales" in prompt:
            last_week = datetime.now() - timedelta(days=7)
            recent_df = df[df["Date"] >= last_week]

            if recent_df.empty:
                return "No sales data available for the last 7 days."

            top_rows = recent_df.sort_values(by="Sales", ascending=False).head(3)
            response = "📈 Top entries with highest sales in the last 7 days:\n"
            for i, row in top_rows.iterrows():
                response += f"- {row['Date'].date()} → {row['Sales']} units sold\n"
            return response.strip()

        return "Sorry, I didn’t understand that command."

    except Exception as e:
        return f"Error processing command: {e}"

#Chatting wiht the bot
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
