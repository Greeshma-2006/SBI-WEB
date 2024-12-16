from flask import Flask, request, jsonify
import joblib
import numpy as np
import pandas as pd
from flask_cors import CORS

# Load the Trained Model
model = joblib.load('fraud_detection_model.pkl')

# Create a Flask App
app = Flask(__name__)

# Enable CORS for cross-origin requests (frontend-backend communication)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow requests from all origins

@app.route('/')
def home():
    return "Fraud Detection API is running!"

# Fraud Detection Endpoint
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Parse JSON Data
        data = request.get_json()

        # Extract values from input
        client_name = data['client_name']
        claim_amount = data['claim_amount']
        claim_reason = data['claim_reason']
        card_details = data['card_details']

        # Validate claim_reason (convert to numeric)
        claim_reason_map = {'accident': 0, 'fire': 1, 'theft': 2}
        claim_reason_numeric = claim_reason_map.get(claim_reason.lower(), -1)

        if claim_reason_numeric == -1:
            return jsonify({'error': 'Invalid claim_reason'}), 400

        # Encode client_name and card_details
        client_name_encoded = pd.factorize([client_name])[0][0]
        card_details_encoded = pd.factorize([card_details])[0][0]

        # Prepare the features for prediction
        features = np.array([[claim_amount, claim_reason_numeric, client_name_encoded, card_details_encoded]])

        # Predict Fraud
        prediction = model.predict(features)[0]

        # Return Prediction
        return jsonify({
            'fraud': bool(prediction),
            'client_name': client_name,
            'claim_amount': claim_amount,
            'claim_reason': claim_reason,
            'card_details': card_details
        })

    except Exception as e:
        # Handle exceptions and return a 500 status code
        return jsonify({'error': str(e)}), 500

# Run the Flask App
if __name__ == '__main__':
    app.run(debug=True)
