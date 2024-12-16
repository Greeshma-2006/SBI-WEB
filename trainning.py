import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# Sample data with client names and card details
data = {
    'client_name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
    'claim_amount': [10000, 50000, 7000, 20000, 100000],
    'claim_reason': ['accident', 'fire', 'theft', 'accident', 'fire'],
    'card_details': ['1234-5678-9876-5432', '2345-6789-8765-4321', '3456-7890-7654-3210', '4567-8901-6543-2109', '5678-9012-5432-1098'],
    'fraud': [0, 1, 0, 0, 1]
}

# Convert data into DataFrame
df = pd.DataFrame(data)

# Convert categorical variables (claim_reason, client_name, card_details) into numeric using simple encoding
df['claim_reason'] = df['claim_reason'].map({'accident': 0, 'fire': 1, 'theft': 2})
df['client_name'] = pd.factorize(df['client_name'])[0]  # Simple encoding for client names
df['card_details'] = pd.factorize(df['card_details'])[0]  # Simple encoding for card details

# Features and labels
X = df[['claim_amount', 'claim_reason', 'client_name', 'card_details']]
y = df['fraud']

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the Random Forest model
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Save the trained model to a file
joblib.dump(model, 'fraud_detection_model.pkl')
print("Model trained and saved successfully.")
