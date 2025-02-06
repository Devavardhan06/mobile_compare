import csv
import pandas as pd
from flask import Flask, render_template, request
from sklearn.neighbors import NearestNeighbors

app = Flask(__name__)

# Load and preprocess the mobile dataset
df = pd.read_csv("mobiles_cleaned.csv")

# Convert numeric features to float
df["Price"] = pd.to_numeric(df["Price"], errors="coerce").fillna(0)
df["Battery Capacity"] = pd.to_numeric(df["Battery Capacity"], errors="coerce").fillna(0)
df["Primary Camera"] = df["Primary Camera"].str.extract("(\d+)").astype(float).fillna(0)  # Extract MP value

# Fill missing processor names with 'Unknown'
df["Processor Type"] = df["Processor Type"].fillna("Unknown").str.strip()

# Standardize processor names
df["Processor Type"] = df["Processor Type"].replace({
    "Mediatek Helio G85": "Helio G85",
    "Dimensity 6020": "MediaTek Dimensity 6020",
    "Snapdragon 695": "Qualcomm Snapdragon 695",
    "A15 Bionic Chip": "Apple A15 Bionic",
    "Helio G37": "MediaTek Helio G37",
    "Dimensity 6100+": "MediaTek Dimensity 6100+",
    "Unisoc Spreadtrum SC9863A1": "Unisoc SC9863A1",
    "Helio G88": "MediaTek Helio G88",
    "Snapdragon 4 Gen 2": "Qualcomm Snapdragon 4 Gen 2"
}, regex=True)

# Print unique processor names for debugging
print("Available Processor Types:", df["Processor Type"].unique())

# Select features for recommendations
features = df[["Price", "Battery Capacity", "Primary Camera"]]

# Train AI Model (K-Nearest Neighbors)
model = NearestNeighbors(n_neighbors=5)
model.fit(features)

def recommend_mobiles(price, battery, camera, processor):
    input_features = [[price, battery, camera]]
    distances, indices = model.kneighbors(input_features)
    recommended_mobiles = df.iloc[indices[0]][["Brand", "Model Name", "Price", "Battery Capacity", "Primary Camera", "Processor Type"]]

    # Filter recommendations by processor preference
    if processor.lower() != "any":
        recommended_mobiles = recommended_mobiles[recommended_mobiles["Processor Type"].str.contains(processor, case=False, na=False)]
    
    print("Recommended Mobiles (After Filtering):")  # Debugging line
    print(recommended_mobiles)

    return recommended_mobiles.to_dict(orient="records")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        price = int(request.form['price'])
        battery = int(request.form['battery'])
        camera = int(request.form['camera'])
        processor = request.form['processor']

        recommendations = recommend_mobiles(price, battery, camera, processor)
        return render_template('recommend.html', recommendations=recommendations)
    except:
        return render_template('index.html', error="Invalid input! Please enter valid values.")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


