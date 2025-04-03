from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pickle
import pandas as pd
import numpy as np
import logging

# Load the model
with open("LinearRegression.pkl", "rb") as file:
    model = pickle.load(file)

app = FastAPI()

# Dummy User Database
users_db = {"yasir": {"password": "1234"}, "admin": {"password": "adminpass"}}

# Logging Setup (Logging to console instead of file)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

# Login Request Model
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
