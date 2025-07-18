import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
import joblib
import os

# ✅ Create models directory inside current working dir
os.makedirs("models", exist_ok=True)

# Load training data
data_path = "data/transactions_labeled.csv"
df = pd.read_csv(data_path)

# Drop non-feature columns
df.drop(columns=["txn_id", "timestamp"], inplace=True)

# Label encode categorical features with 'unknown' class
categorical_cols = ["txn_type", "source_account", "dest_account", "status", "ip_address", "device_id"]
label_encoders = {}

for col in categorical_cols:
    le = LabelEncoder()
    df[col] = df[col].astype(str)
    le.fit(df[col])

    # Add "unknown" to encoder classes if not present
    if "unknown" not in le.classes_:
        le.classes_ = np.append(le.classes_, "unknown")

    df[col] = le.transform(df[col])
    label_encoders[col] = le

# Encode target variable
target_encoder = LabelEncoder()
df["label"] = target_encoder.fit_transform(df["label"])  # fraud → 1, normal → 0

# Split into features and target
X = df.drop(columns=["label"])
y = df["label"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

# Train Random Forest classifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate and display results
y_pred = model.predict(X_test)
print("📊 Classification Report:\n")
print(classification_report(y_test, y_pred))

# ✅ Save model and encoders inside ./models/
joblib.dump(model, "models/fraud_model.pkl")
joblib.dump(label_encoders, "models/label_encoders.pkl")
joblib.dump(target_encoder, "models/target_encoder.pkl")

print("\n✅ Model training complete. Files saved in 'models/' directory.")
