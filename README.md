# Voice Activated Inventory Assistant
This is a smart inventory assistant that integrates your data with an AI model using Model Context Protocol(MCP). 

# Description
It uses MCP (Model Context Protocol) to link GPT-style language understanding with structured inventory data and a predictive model. All voice input is processed offline, and the assistant can take actions based on your spoken prompts.

Overview about this Project?
To build an offline, voice-enabled analytics tool

To explore GPT4All + inventory Data + predictive modeling integration

To create a smart agent that’s usable in real retail scenarios

Future Improvements

🛠 Installation
Make sure you have Python 3.8+ installed.

Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt

Place your CSV file:

File: Advertising_Extended.csv

Required columns:
TV, Radio, Newspaper, Sales, Stock_Available, Stock_Used, Restock_Threshold, Reorder_Quantity, Stock_Replenished, Date

Run the assistant:

bash
Copy
Edit
python assistant.py

How to Use the Project
Open command prompt and enter: uvicorn mains:app --reload to run the fastAPI code
Again open the command prompt and enter: streamlit run frontend.py to run the frontend code

You enter the login space.
Enter the credentials like this:
![Login](https://github.com/user-attachments/assets/16ee681a-b05b-4274-8e0e-d55e88f6ff33)

Once you are logged in try predicting the model like this:
![Prediction](https://github.com/user-attachments/assets/5365db8a-4011-4ae3-950a-8a1e6bc7878e)

Then try using the voice assistant:
Once the assistant is running:

It will listen for your voice command

It will process your query using MCP + GPT4All

Then it will:

Respond using text-to-speech

Trigger backend logic (e.g., alert, prediction, analytics)

Example Commands:
"Predict sales for this week"

"Give me a stock alert"

"What were last week's top selling products?"

"Exit" – to close the assistant
![Voice assistant](https://github.com/user-attachments/assets/851e767f-a3af-4768-9133-69a10cdd4bc6)


All responses are spoken back to you using TTS.

Features
Voice command recognition

Predict sales from ad budgets

Show top selling products from last 7 days

Alert when stock is below restock threshold

GPT-style responses using GPT4All(offline)

Works on local .csv data — no database required

Easy to extend with FastAPI or Streamlit

Tech Stack

Component	Description
gpt4all	Offline conversational model (TinyLLaMA)
speech_recognition	Convert voice to text
pyttsx3	Speak text output (TTS)
pandas	CSV and inventory logic
datetime	For weekly filtering
FastAPI (optional)	Add RESTful endpoints for deployment

Future Improvements:
Add user authentication with face recognition

Replace CSV with SQLite or MongoDB

Streamlit dashboard for live analytics

Wake-word feature (“Hey Inventory!”)

