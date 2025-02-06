from flask import Flask, request, jsonify
import pandas as pd
import pickle
from sklearn.neighbors import NearestNeighbors

# Load mobile dataset (Ensure dataset.csv is in the same directory)
df = pd.read_csv('mobile_data.csv')

# Define features for recommendation
features = ['price', 'camera', 'battery', 'ram', 'performance']
X = df[features]

# Train KNN model
knn = NearestNeighbors(n_neighbors=5, metric='euclidean')
knn.fit(X)

# Save trained model
with open('mobile_recommendation_model.pkl', 'wb') as model_file:
    pickle.dump(knn, model_file)

# Load model
with open('mobile_recommendation_model.pkl', 'rb') as model_file:
    knn = pickle.load(model_file)

app = Flask(__name__)

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    user_input = [[data['price'], data['camera'], data['battery'], data['ram'], data['performance']]]
    
    distances, indices = knn.kneighbors(user_input)
    recommendations = df.iloc[indices[0]].to_dict(orient='records')
    
    return jsonify({'recommendations': recommendations})

if __name__ == '__main__':
    app.run(debug=True)
