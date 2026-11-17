import os
import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier

# Seed for reproducibility
np.random.seed(42)

def generate_synthetic_data(num_samples=3000):
    # Features
    # weight_kg: 0.05 to 50 kg
    weight_kg = np.random.uniform(0.05, 50.0, num_samples)
    # declared_value: 50 to 50000 INR
    declared_value = np.random.uniform(50.0, 50000.0, num_samples)
    # is_same_city: 0 or 1
    is_same_city = np.random.choice([0, 1], size=num_samples, p=[0.7, 0.3])
    
    # Target Labels: 0 = LOW, 1 = MEDIUM, 2 = HIGH
    y = np.zeros(num_samples, dtype=int)
    
    for i in range(num_samples):
        w = weight_kg[i]
        val = declared_value[i]
        same_city = is_same_city[i]
        
        # Rule 1: High value per weight ratio
        val_per_kg = val / max(w, 0.1)
        if val_per_kg > 5000:
            y[i] = 2 # HIGH
        # Rule 3: Very low weight + high value
        elif w < 0.1 and val > 2000:
            y[i] = 2 # HIGH
        # Rule 2: Same city + high value
        elif same_city == 1 and val > 10000:
            y[i] = 1 # MEDIUM
        else:
            y[i] = 0 # LOW
            
        # Add 3% noise to simulate a real ML dataset
        if np.random.rand() < 0.03:
            y[i] = np.random.choice([0, 1, 2])
            
    X = np.column_stack((weight_kg, declared_value, is_same_city))
    return X, y

def train_and_save():
    print("Generating synthetic shipment data for ML training...")
    X, y = generate_synthetic_data(3000)
    
    print("Training RandomForestClassifier...")
    clf = RandomForestClassifier(n_estimators=100, max_depth=6, random_state=42)
    clf.fit(X, y)
    
    # Check training accuracy
    train_acc = clf.score(X, y)
    print(f"Model trained with self-accuracy: {train_acc:.4f}")
    
    # Ensure ml directory exists
    ml_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(ml_dir, "fraud_model.joblib")
    
    print(f"Saving ML model to {model_path}...")
    # Save the model
    joblib.dump(clf, model_path)
    print("Model saved successfully!")

if __name__ == "__main__":
    train_and_save()
