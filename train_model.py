import pandas as pd
import joblib
from sklearn.ensemble import IsolationForest
from sklearn.model_selection import train_test_split
import os

print("[*] Loading the simulated USB dataset...")
# Load the data we generated yesterday
df = pd.read_csv("data/usb_simulated_logs.csv")

# Select the behavioral features for the AI to analyze:
# 1. Keystroke Delay (fast injection speeds)
# 2. Transfer Volume (massive data exfiltration)
# 3. Entropy (encrypted ransomware/malware files)
features = ["keystroke_delay", "transfer_volume", "entropy"]
X = df[features]
y = df["is_anomaly"] # True labels for evaluation

# Split data into 80% training and 20% testing to verify accuracy
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print("[*] Training the Isolation Forest Anomaly Detection model...")
# Contamination represents the expected percentage of malicious entries (approx 7%)
model = IsolationForest(contamination=0.07, random_state=42)
model.fit(X_train)

# Test the model's predictions (-1 indicates an anomaly, 1 indicates normal)
predictions = model.predict(X_test)
# Convert model output format to match our labels (0 for safe, 1 for anomaly)
converted_predictions = [1 if pred == -1 else 0 for pred in predictions]

# Calculate accuracy
correct_matches = sum(1 for p, t in zip(converted_predictions, y_test) if p == t)
accuracy = (correct_matches / len(y_test)) * 100
print(f"[+] Model Training Complete! Testing Accuracy: {accuracy:.2f}%")

# Save the trained AI model weights so our background listener can use it live
os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/usb_threat_detector.pkl")
print("[+] AI engine saved successfully at: models/usb_threat_detector.pkl")