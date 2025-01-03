import frappe
from frappe.tests.utils import FrappeTestCase
from datetime import datetime

class TestEarthquakeData(FrappeTestCase):
    def setUp(self):
        # Create test earthquake data
        self.test_earthquake = {
            "doctype": "Earthquake Data",
            "id": "test123",
            "magnitude": 5.6,
            "place": "Test Location, Country",
            "latitude": 34.0522,
            "longitude": -118.2437,
            "depth": 10.5,
            "time": datetime.now(),
            "significance": 650,
            "coordinates": f"{{ 'type': 'Point', 'coordinates': [-118.2437, 34.0522] }}"
        }
        
    def tearDown(self):
        # Clean up test data
        if frappe.db.exists("Earthquake Data", "test123"):
            frappe.delete_doc("Earthquake Data", "test123")
            
    def test_earthquake_creation(self):
        earthquake = frappe.get_doc(self.test_earthquake)
        earthquake.insert()
        
        print("Test: Earthquake creation")
        self.assertTrue(frappe.db.exists("Earthquake Data", "test123"))
        
    def test_required_fields(self):
        # Test missing required field
        incomplete_earthquake = self.test_earthquake.copy()
        del incomplete_earthquake["magnitude"]
        
        with self.assertRaises(frappe.ValidationError):
            frappe.get_doc(incomplete_earthquake).insert()
        print("Test: Missing required field (magnitude)")
            
    def test_coordinate_validation(self):
        earthquake = frappe.get_doc(self.test_earthquake)
        earthquake.insert()
        
        # Verify coordinates match latitude/longitude
        saved_earthquake = frappe.get_doc("Earthquake Data", "test123")
        self.assertEqual(saved_earthquake.latitude, 34.0522)
        self.assertEqual(saved_earthquake.longitude, -118.2437)
        print("Test: Coordinates validation passed")
        
    def test_magnitude_range(self):
        # Test invalid magnitude
        invalid_earthquake = self.test_earthquake.copy()
        invalid_earthquake["magnitude"] = -1.0
        
        with self.assertRaises(frappe.ValidationError):
            frappe.get_doc(invalid_earthquake).insert()
        print("Test: Invalid magnitude range")
            
    def test_unique_id(self):
        # Create first earthquake
        earthquake1 = frappe.get_doc(self.test_earthquake)
        earthquake1.insert()
        
        # Try to create another with same ID
        earthquake2 = self.test_earthquake.copy()
        
        with self.assertRaises(frappe.DuplicateEntryError):
            frappe.get_doc(earthquake2).insert()
        print("Test: Unique ID check passed")
