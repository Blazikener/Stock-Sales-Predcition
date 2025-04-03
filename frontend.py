import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.title("Login to Prediction System")

# Login Section
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

# Prediction Section (only visible after login)
if "logged_in" in st.session_state and st.session_state["logged_in"]:
    st.subheader("Enter Data for Prediction")

    TV = st.number_input("TV Budget", value=1000.5)
    Radio = st.number_input("Radio Budget", value=500.25)
    Newspaper = st.number_input("Newspaper Budget", value=200.75)
    Stock_Available = st.number_input("Stock Available", value=50)
    Stock_Used = st.number_input("Stock Used", value=10)
    Restock_Threshold = st.number_input("Restock Threshold", value=5)
    Reorder_Quantity = st.number_input("Reorder Quantity", value=20)
    Stock_Replenished = st.number_input("Stock Replenished", value=15)

    # Properly formatted date input
    date = st.date_input("Select Date")
    formatted_date = date.strftime("%Y-%m-%d")  # Ensures correct format

    # Display formatted date for debugging
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


