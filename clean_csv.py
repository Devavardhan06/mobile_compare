import pandas as pd

# Load the CSV file
csv_file = "mobiles.csv"
df = pd.read_csv(csv_file, encoding="utf-8")

# Fill missing numeric values with 0
num_cols = ["Price", "No_of_Ratings", "No_of_Reviews", "Battery Capacity", "Weight"]
for col in num_cols:
    if col in df.columns:
        df[col] = df[col].fillna(0)

# Fill missing text values with "N/A"
df.fillna("N/A", inplace=True)

# Save the cleaned CSV file
df.to_csv("mobiles_cleaned.csv", index=False, encoding="utf-8")

print("✅ Missing values fixed! New file saved as 'mobiles_cleaned.csv'.")
