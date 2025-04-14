import streamlit as st
import requests
import subprocess
import os

API_URL = "http://127.0.0.1:8000"

st.title("Login to Prediction System")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    response = requests.post(f"{API_URL}/login", json={"username": username, "password": password})
    if response.status_code == 200:
        st.success(response.json()["message"])
        st.session_state["logged_in"] = True
        st.session_state["username"] = username
    else:
        st.error("Invalid credentials!")

if "logged_in" in st.session_state and st.session_state["logged_in"]:
    if st.button("start Voice Assistant"):
        script_path = os.path.abspath("voice_assistant_mcp.py") 
        subprocess.Popen(["python", script_path], creationflags=subprocess.CREATE_NEW_CONSOLE)
        st.info("Voice Assistant started in a new window!")

    
    st.subheader("Enter Data for Prediction")

    TV = st.text_input("Enter TV Budget")
    Radio = st.text_input("Enter Radio Budget")
    Newspaper = st.text_input("Enter Newspaper Budget")
    Stock_Available = st.text_input("Enter Stock Available")
    Stock_Used = st.text_input("Enter Stock Used")
    Restock_Threshold = st.text_input("Enter Restock Threshold")
    Reorder_Quantity = st.text_input("Enter Reorder Quantity")
    Stock_Replenished = st.text_input("Enter Stock Replenished")


    date = st.date_input("Select Date")
    formatted_date = date.strftime("%Y-%m-%d")  
    st.write(f"Formatted Date: {formatted_date}")

    if st.button("Predict"):
        data = {
            "TV": TV, "Radio": Radio, "Newspaper": Newspaper,
            "Stock_Available": Stock_Available, "Stock_Used": Stock_Used,
            "Restock_Threshold": Restock_Threshold, "Reorder_Quantity": Reorder_Quantity,
            "Stock_Replenished": Stock_Replenished, "Date": formatted_date
        }

        response = requests.post(f"{API_URL}/predict", json=data)

        if response.status_code == 200:
            st.success(f"Predicted Sales: {response.json()['prediction']}")
        else:
            st.error("Prediction failed!")


