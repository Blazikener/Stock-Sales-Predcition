from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import pandas as pd
import numpy as np

# Load the model
with open("LinearRegression.pkl", "rb") as file:
    model = pickle.load(file)

app = FastAPI()

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
        # Convert Date to numerical format
        date_obj = pd.to_datetime(data.Date, format="%Y-%m-%d").timestamp()

        # Prepare input features
        features = np.array([[data.TV, data.Radio, data.Newspaper, data.Stock_Available,
                              data.Stock_Used, data.Restock_Threshold, data.Reorder_Quantity,
                              data.Stock_Replenished, date_obj]])

        # Make prediction
        prediction = model.predict(features)

        return {"prediction": prediction.tolist()}  # Convert to JSON serializable format

    except Exception as e:
        return {"error": str(e)}  # Catch errors and return as JSON
