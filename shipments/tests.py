import os
from decimal import Decimal
from django.test import TestCase
from ml.fraud_detector import calculate_risk_score
from ml.train_model import train_and_save

class FraudDetectorTestCase(TestCase):
    def setUp(self):
        # Get path to the model file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.model_path = os.path.abspath(os.path.join(current_dir, "..", "ml", "fraud_model.joblib"))
        
        # Delete model file if it exists to test the fallback mechanism
        if os.path.exists(self.model_path):
            try:
                os.remove(self.model_path)
            except Exception:
                pass
                
        # Reset the global model loader state in ml.fraud_detector
        import ml.fraud_detector
        ml.fraud_detector._MODEL = None
        ml.fraud_detector._MODEL_LOADED = False

    def tearDown(self):
        # Clean up the model file after tests
        if os.path.exists(self.model_path):
            try:
                os.remove(self.model_path)
            except Exception:
                pass

    def test_rule_based_fallback_high_value_per_kg(self):
        # Rule 1: High value per kg -> HIGH
        # weight: 1.0kg, value: 6000 INR -> ratio 6000 > 5000
        risk, details = calculate_risk_score(Decimal("1.0"), Decimal("6000"), "Mumbai", "Delhi")
        self.assertEqual(risk, "HIGH")
        self.assertIn("High value/weight ratio", details)
        self.assertIn("ML model not trained", details)

    def test_rule_based_fallback_same_city(self):
        # Rule 2: Same city + high value -> MEDIUM
        # weight: 10.0kg, value: 15000 INR -> Mumbai to Mumbai
        risk, details = calculate_risk_score(Decimal("10.0"), Decimal("15000"), "Mumbai", "Mumbai")
        self.assertEqual(risk, "MEDIUM")
        self.assertIn("High-value shipment within same city", details)

    def test_rule_based_fallback_suspicious_package(self):
        # Rule 3: Very low weight + high value -> HIGH
        # weight: 0.05kg, value: 3000 INR
        risk, details = calculate_risk_score(Decimal("0.05"), Decimal("3000"), "Mumbai", "Delhi")
        self.assertEqual(risk, "HIGH")
        self.assertIn("Suspiciously light, high-value package", details)

    def test_ml_model_prediction(self):
        # Train and save the model
        train_and_save()
        
        # Verify model file was generated
        self.assertTrue(os.path.exists(self.model_path))
        
        # Reset the loader state to force loading of the new model
        import ml.fraud_detector
        ml.fraud_detector._MODEL = None
        ml.fraud_detector._MODEL_LOADED = False
        
        # Test prediction using ML model
        # Test a high-risk package
        risk, details = calculate_risk_score(Decimal("0.05"), Decimal("3000"), "Mumbai", "Delhi")
        self.assertEqual(risk, "HIGH")
        self.assertIn("AI Model prediction: HIGH", details)
        
        # Test a low-risk package
        risk, details = calculate_risk_score(Decimal("2.0"), Decimal("50"), "Mumbai", "Delhi")
        self.assertEqual(risk, "LOW")
        self.assertIn("AI Model prediction: LOW", details)
