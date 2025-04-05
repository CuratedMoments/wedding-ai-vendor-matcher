from flask import Flask, request, jsonify
import pandas as pd
from itertools import product
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "💍 Curated Moments Budget API is running!"

@app.route('/get-combinations', methods=['POST'])
def get_combinations():
    try:
        # Get the budget and return top combinations
        data = request.get_json()
        budget = int(data.get("budget", 0))

        # Load uploaded Excel file
        excel_file = "TESTCASE1.xlsx"
        sheet_names = ["Tab1", "Tab2", "Tab3"]
        sheets_data = {}

        for sheet in sheet_names:
            df = pd.read_excel(excel_file, sheet_name=sheet)
            sheets_data[sheet] = df

        # Generate combinations
        combinations = list(product(*(sheets_data[sheet].to_dict('records') for sheet in sheet_names)))
        valid_combinations = []

        for combo in combinations:
            total_price = sum(service['Price'] for service in combo)
            if total_price <= budget:
                valid_combinations.append(combo)

        # Format top 10 results
        if not valid_combinations:
            return jsonify({"output": "No valid combinations found within the budget."})

        results = []
        for combo in valid_combinations[:10]:
            desc = ""
            for service in combo:
                desc += f"{service['Name']} ({service['Location']}): ₹{service['Price']}\n"
            desc += f"Total: ₹{sum(s['Price'] for s in combo)}\n"
            results.append(desc)

        return jsonify({"output": "\n\n".join(results)})
    
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run()
