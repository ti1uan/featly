# tests/test_feature.py
import unittest
from datetime import datetime
from featly.core.feature.defs import ValueType, FeatureType
from featly.core.feature.feature import Feature
from pydantic import ValidationError

class TestFeature(unittest.TestCase):
    def setUp(self):
        """Setup basic feature for tests"""
        self.valid_feature_data = {
            "name": "user_age",
            "description": "Age of the user",
            "value_type": ValueType.INT,
            "feature_type": FeatureType.NUMERICAL,
            "entity": "user",
            "tags": ["demographic"],
            "metadata": {"min_value": 0, "max_value": 120}
        }

    def test_create_feature(self):
        """Test basic feature creation"""
        feature = Feature(**self.valid_feature_data)
        
        self.assertEqual(feature.name, "user_age")
        self.assertEqual(feature.value_type, ValueType.INT)
        self.assertEqual(feature.feature_type, FeatureType.NUMERICAL)
        self.assertEqual(feature.entity, "user")
        self.assertEqual(feature.version, "1.0.0")  # default version
        self.assertIsInstance(feature.created_at, datetime)
        self.assertIsNone(feature.updated_at)

    def test_missing_required_fields(self):
        """Test that required fields raise ValidationError when missing"""
        invalid_data = {
            "name": "user_age",
            # missing value_type
            "feature_type": FeatureType.NUMERICAL,
            "entity": "user"
        }
        
        with self.assertRaises(ValidationError):
            Feature(**invalid_data)

    def test_update_version(self):
        """Test version update functionality"""
        feature = Feature(**self.valid_feature_data)
        original_created_at = feature.created_at
        
        # Wait a small amount to ensure different datetime
        import time
        time.sleep(0.001)
        
        feature.update_version("2.0.0")
        
        self.assertEqual(feature.version, "2.0.0")
        self.assertIsNotNone(feature.updated_at)
        self.assertNotEqual(feature.updated_at, original_created_at)
        self.assertEqual(feature.created_at, original_created_at)

    def test_json_serialization(self):
        """Test JSON serialization of feature"""
        feature = Feature(**self.valid_feature_data)
        json_data = feature.json()
        
        # Deserialize back to feature
        recreated_feature = Feature.parse_raw(json_data)
        
        self.assertEqual(recreated_feature.name, feature.name)
        self.assertEqual(recreated_feature.value_type, feature.value_type)
        self.assertEqual(recreated_feature.feature_type, feature.feature_type)

    def test_invalid_value_type(self):
        """Test that invalid value_type raises ValidationError"""
        invalid_data = self.valid_feature_data.copy()
        invalid_data["value_type"] = "INVALID_TYPE"
        
        with self.assertRaises(ValidationError):
            Feature(**invalid_data)

if __name__ == '__main__':
    unittest.main()