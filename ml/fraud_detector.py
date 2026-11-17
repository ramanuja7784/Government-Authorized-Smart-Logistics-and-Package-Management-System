import os
import joblib
import numpy as np

# Global variables for model
_MODEL = None
_MODEL_LOADED = False

def load_ml_model():
    global _MODEL, _MODEL_LOADED
    if _MODEL_LOADED:
        return _MODEL
    
    ml_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(ml_dir, "fraud_model.joblib")
    
    if os.path.exists(model_path):
        try:
            # We must load the model using joblib. Since we trained it using scikit-learn,
            # this will deserialize the RandomForestClassifier.
            _MODEL = joblib.load(model_path)
            _MODEL_LOADED = True
            print("ML model loaded successfully.")
        except Exception as e:
            print(f"Error loading ML model: {e}")
            _MODEL = None
            _MODEL_LOADED = False
    else:
        _MODEL = None
        _MODEL_LOADED = False
        
    return _MODEL

def calculate_risk_score(weight_kg, declared_value, source_city, dest_city):
    """
    ML-based fraud detection with rule-based fallback.
    Returns: (risk_score, risk_details)
    """
    # Safe float conversions
    try:
        weight = float(weight_kg)
    except (ValueError, TypeError):
        weight = 0.1
    weight = max(weight, 0.01) # Avoid division by zero
    
    try:
        value = float(declared_value)
    except (ValueError, TypeError):
        value = 0.0

    # Clean city comparison
    s_city = str(source_city).strip().lower()
    d_city = str(dest_city).strip().lower()
    is_same_city = 1 if (s_city == d_city and s_city != "") else 0

    # Rule-based calculation (for fallback and detail generation)
    rule_reasons = []
    rule_risk = "LOW"

    # Rule 1: High value per kg
    value_per_kg = value / weight
    if value_per_kg > 5000:
        rule_risk = "HIGH"
        rule_reasons.append(f"High value/weight ratio (₹{value_per_kg:.0f}/kg)")

    # Rule 2: Same city + high value
    if is_same_city == 1 and value > 10000:
        if rule_risk == "LOW":
            rule_risk = "MEDIUM"
        rule_reasons.append("High-value shipment within same city")

    # Rule 3: Very low weight + high value
    if weight < 0.1 and value > 2000:
        rule_risk = "HIGH"
        rule_reasons.append("Suspiciously light, high-value package")

    # Try loading the ML model
    model = load_ml_model()
    
    if model is not None:
        try:
            # Prepare feature array: [[weight_kg, declared_value, is_same_city]]
            features = np.array([[weight, value, is_same_city]], dtype=float)
            prediction = int(model.predict(features)[0])
            
            # Map prediction class back to risk labels
            # 0 -> LOW, 1 -> MEDIUM, 2 -> HIGH
            class_map = {0: "LOW", 1: "MEDIUM", 2: "HIGH"}
            ml_risk = class_map.get(prediction, "LOW")
            
            # Generate details
            details_list = [f"AI Model prediction: {ml_risk}"]
            if rule_reasons:
                details_list.append(f"Rule triggers: {'; '.join(rule_reasons)}")
            else:
                details_list.append("No manual rules triggered")
                
            return ml_risk, " | ".join(details_list)
        except Exception as e:
            # If prediction fails, fall back to rule_risk
            fallback_details = f"Rule-based Fallback (ML error: {e})"
            if rule_reasons:
                fallback_details += f" - {'; '.join(rule_reasons)}"
            return rule_risk, fallback_details
    else:
        # Fallback to rules if model is not trained yet
        fallback_details = "Rule-based Fallback (ML model not trained)"
        if rule_reasons:
            fallback_details += f" - {'; '.join(rule_reasons)}"
        else:
            fallback_details += " - No risks detected"
        return rule_risk, fallback_details
