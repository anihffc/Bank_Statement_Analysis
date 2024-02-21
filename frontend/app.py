# frontend/app.py

import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# Replace with the actual endpoint of your Flask API
API_ENDPOINT = "http://127.0.0.1:5000/api/analyze"

# Streamlit UI code
st.title("Bank Statement Analysis")

# Dummy user data for demonstration
user_data = {
    "username": "JohnDoe",
    "password": "password123",
    # Add more user data as needed
}

# Login section
username = st.text_input("Username:")
password = st.text_input("Password:", type="password")
login_button = st.button("Login")

if login_button:
    # Validate user credentials (replace with your actual validation logic)
    if username == user_data["username"] and password == user_data["password"]:
        st.success("Login successful!")

        # Fetch analysis results from the Flask backend API
        response = requests.post(API_ENDPOINT, json={})
        analysis_results = response.json()

        # Display analysis results
        st.subheader("Summary:")
        st.write(f"Total Transactions: {analysis_results['total_transactions']}")
        st.write(f"Total Debits: {analysis_results['total_debits']}")
        st.write(f"Total Credits: {analysis_results['total_credits']}")
        st.write(f"Average Transaction Amount: {analysis_results['average_transaction_amount']}")

        st.subheader("Transaction Extremes:")
        st.write(f"Largest Transaction: {analysis_results['largest_transaction']}")
        st.write(f"Smallest Transaction: {analysis_results['smallest_transaction']}")

        st.subheader("Transaction Types:")
        st.write(f"Transaction Types: {analysis_results['transaction_types']}")

        st.subheader("Transactions Data:")
        transactions_df = pd.DataFrame(analysis_results['transactions_data'])
        st.dataframe(transactions_df)

        st.subheader("Transaction Period:")
        st.write(f"Start Date: {analysis_results['start_date']}")
        st.write(f"End Date: {analysis_results['end_date']}")

        st.subheader("Transaction Frequency:")
        st.bar_chart(analysis_results['transaction_frequency'])

        st.subheader("Transaction Modes:")
        st.write(f"Transaction Modes: {analysis_results['transaction_modes']}")

        st.subheader("Transactions by Mode:")
        st.bar_chart(analysis_results['transactions_by_mode'])
    else:
        st.error("Invalid credentials. Please try again.")