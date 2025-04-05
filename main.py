from flask import Flask, request, jsonify
import pandas as pd
import random
from itertools import product

app = Flask(__name__)

PROBABILITY_THRESHOLD = 0.3  # Control output size

@app.route('/api/match-vendors', methods=['POST'])
def match_vendors():
    data = request.get_json()
    budget = int(data.get('budget', 0))
    location = data.get('location')
    services = data.get('services', [])

    # Load your Excel
    df1 = pd.read_excel("wed_photography_decor-data_dec26.xlsx", sheet_name="Tab1")
    df2 = pd.read_excel("wed_photography_decor-data_dec26.xlsx", sheet_name="Tab2")
    df3 = pd.read_excel("wed_photography_decor-data_dec26.xlsx", sheet_name="Tab3")

    dfs = [df1.astype(str), df2.astype(str), df3.astype(str)]
    combined = [df.apply(lambda r: " | ".join(r), axis=1).tolist() for df in dfs]
    combos = list(product(*combined))
    filtered = [c for c in combos if random.random() < PROBABILITY_THRESHOLD]

    results = []
    for combo in filtered:
        row = []
        for part in combo:
            row.extend(part.split(" | "))
        try:
            total = sum(float(row[i]) for i in [3, 7, 11])  # Col4,8,12
        except:
            total = 0
        if total <= budget:
            results.append({
                "Photographer": row[0],
                "Decor": row[4],
                "Caterer": row[8],
                "Total": total
            })

    return jsonify({"matches": results})

if __name__ == '__main__':
    app.run()
