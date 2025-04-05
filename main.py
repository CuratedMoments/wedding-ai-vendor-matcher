import pandas as pd
import random
from itertools import product
import sys
import os

# Read arguments passed to the script
# Example usage: python script4.py TESTCASE1.xlsx 250000
if len(sys.argv) != 3:
    print("Usage: python script4.py <filename> <sum_threshold>")
    sys.exit(1)

file_path = sys.argv[1]
threshold = int(sys.argv[2])
print(f"Processing file: {file_path} with threshold: {threshold}")

# Define the expected sheet names
sheet_names = ["Tab1", "Tab2", "Tab3"]
sheets_data = {}

# Load sheets and validate their content
try:
    for sheet in sheet_names:
        df = pd.read_excel(file_path, sheet_name=sheet)
        if not {'Name', 'Price', 'Location'}.issubset(df.columns):
            print(f"Error: Sheet '{sheet}' must contain 'Name', 'Price', and 'Location' columns.")
            sys.exit(1)
        sheets_data[sheet] = df
except Exception as e:
    print(f"Error reading Excel file: {e}")
    sys.exit(1)

# Generate combinations from all sheets
combinations = list(product(*(sheets_data[sheet].to_dict('records') for sheet in sheet_names)))

# Filter valid combinations under the budget threshold
valid_combinations = []
for combo in combinations:
    total_price = sum(service['Price'] for service in combo)
    if total_price <= threshold:
        valid_combinations.append(combo)

# Save results to a file
output_file = "valid_combinations_output.txt"
with open(output_file, "w", encoding="utf-8") as f:
    if not valid_combinations:
        f.write("No valid combinations found within budget.\n")
    else:
        f.write(f"Found {len(valid_combinations)} valid combinations:\n")
        for idx, combo in enumerate(valid_combinations[:10]):  # Save top 10 options
            f.write("---\n")
            for service in combo:
                f.write(f"{service['Name']} ({service['Location']}): ₹{service['Price']}\n")
            f.write(f"Total: ₹{sum(service['Price'] for service in combo)}\n")
            f.write("\n")

print(f"Results saved to {output_file}")
