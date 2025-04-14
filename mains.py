from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pickle
import pandas as pd
import numpy as np
import logging
from gpt4all import GPT4All
import pyttsx3
import speech_recognition as sr
import threading

with open("LinearRegression.pkl", "rb") as file:
    model = pickle.load(file)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

users_db = {"yasir": {"password": "1234"}, "admin": {"password": "adminpass"}}

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

class UserLogin(BaseModel):
    username: str
    password: str

@app.post("/login")
def login(user: UserLogin):
    if user.username not in users_db or users_db[user.username]["password"] != user.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    logging.info(f"User {user.username} logged in")
    return {"message": f"Welcome {user.username}!"}

# Prediction Request Model
class InputData(BaseModel):
    TV: float
    Radio: float
    Newspaper: float
    Stock_Available: int
    Stock_Used: float
    Restock_Threshold: int
    Reorder_Quantity: int
    Stock_Replenished: int
    Date: str

@app.get("/")
def greet():
    return {"message": "Hello"}

@app.post('/predict')
def predict(data: InputData):
    try:
        date_obj = pd.to_datetime(data.Date.strip(), format="%Y-%m-%d").timestamp()
        features = np.array([[data.TV, data.Radio, data.Newspaper, data.Stock_Available,
                              data.Stock_Used, data.Restock_Threshold, data.Reorder_Quantity,
                              data.Stock_Replenished, date_obj]])
        prediction = model.predict(features)
        return {"prediction": prediction.tolist()}
    except Exception as e:
        logging.error(f"Prediction error: {str(e)}")
        return {"error": str(e)}

@app.post("/start-voice-assistant")
async def start_voice_assistant():
    thread = threading.Thread(target=run_voice_assistant)
    thread.start()
    return {"message": "Voice assistant started"}


def run_voice_assistant():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    def speak(text):
        print("Bot:", text)
        tts_engine.say(text)
        tts_engine.runAndWait()

    with gpt_model.chat_session() as session:
        while True:
            try:
                with mic as source:
                    print("Listening for command...")
                    recognizer.adjust_for_ambient_noise(source)
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)

                try:
                    prompt = recognizer.recognize_google(audio)
                    print("You:", prompt)
                except:
                    speak("Sorry, I didn't catch that.")
                    continue

                if "exit" in prompt.lower():
                    speak("Goodbye!")
                    break

                if "stock" in prompt.lower():
                    latest = inventory_df.iloc[-1]
                    speak(f"Currently, {latest['Stock_Available']} units are available.")
                elif "top selling" in prompt.lower() or "last week" in prompt.lower():
                    inventory_df['Date'] = pd.to_datetime(inventory_df['Date'])
                    last_week = inventory_df[inventory_df["Date"] > datetime.now() - pd.Timedelta(days=7)]
                    top = last_week.sort_values("Sales", ascending=False).head(1)
                    speak(f"Top product last week had {top['Sales'].values[0]} sales.")
                else:
                    response = session.generate(prompt, temp=0.7)
                    speak(response)

            except Exception as e:
                print("Error:", e)
                break



            












