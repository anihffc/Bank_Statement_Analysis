# backend/analysis.py

import pandas as pd
from bson import ObjectId
import json

def analyze_bank_statement(statement_json):
    # Extracting relevant information from the provided JSON structure
    account_info = statement_json.get("Account", {})
    transactions_info = account_info.get("Transactions", {}).get("Transaction", [])

    # Creating a DataFrame for easier analysis
    transactions_df = pd.DataFrame(transactions_info)

    # Convert amount and current balance to numeric values
    transactions_df["amount"] = pd.to_numeric(transactions_df["amount"])
    transactions_df["currentBalance"] = pd.to_numeric(transactions_df["currentBalance"])

    # Extracted analysis results
    analysis_results = {
        "total_transactions": len(transactions_df),
        "total_debits": transactions_df[transactions_df["type"] == "DEBIT"]["amount"].sum(),
        "total_credits": transactions_df[transactions_df["type"] == "CREDIT"]["amount"].sum(),
        "average_transaction_amount": transactions_df["amount"].mean(),
        "largest_transaction": transactions_df.loc[transactions_df["amount"].idxmax()].to_dict(),
        "smallest_transaction": transactions_df.loc[transactions_df["amount"].idxmin()].to_dict(),
        "transaction_types": transactions_df["type"].unique().tolist(),
        "transactions_data": transactions_df.sort_values(by="transactionTimestamp").to_dict(orient="records"),
        "start_date": transactions_df["valueDate"].min(),
        "end_date": transactions_df["valueDate"].max(),
        "transaction_frequency": transactions_df["valueDate"].value_counts().to_dict(),
        "transaction_modes": transactions_df["mode"].unique().tolist(),
        "transactions_by_mode": transactions_df.groupby("mode").size().to_dict()
    }

    # Function to recursively convert ObjectId to string
    def convert_object_ids(obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        elif isinstance(obj, list):
            return [convert_object_ids(item) for item in obj]
        elif isinstance(obj, dict):
            return {key: convert_object_ids(value) for key, value in obj.items()}
        return obj

    # Recursively convert ObjectId to string in all nested structures
    analysis_results = convert_object_ids(analysis_results)

    # Serialize the results to JSON explicitly
    results_json = json.dumps(analysis_results)
    return json.loads(results_json)