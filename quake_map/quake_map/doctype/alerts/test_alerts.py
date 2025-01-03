# Copyright (c) 2024, Seemab and Contributors
# See license.txt

import frappe
from frappe.tests.utils import FrappeTestCase

class TestAlerts(FrappeTestCase):
    def test_register_alert(self):
        # Test registering a new alert
        email = "test@example.com"
        region = "California"
        
        response = frappe.get_doc({
            "doctype": "Alerts",
            "email": email,
            "region": region
        }).insert()
        
        print(f"Test: Register alert for {email} in {region}")
        
        self.assertEqual(response.email, email, f"Expected email to be {email}, but got {response.email}")
        self.assertEqual(response.region, region, f"Expected region to be {region}, but got {response.region}")
        print(f"Alert registered successfully for {email} in {region}")

    def test_duplicate_alert(self):
        # Test that duplicate alerts are prevented
        email = "duplicate@example.com"
        region = "California"
        
        # First insert
        frappe.get_doc({
            "doctype": "Alerts",
            "email": email,
            "region": region
        }).insert()
        
        print(f"Test: Register duplicate alert for {email} in {region}")
        
        # Try inserting again
        try:
            frappe.get_doc({
                "doctype": "Alerts",
                "email": email,
                "region": region
            }).insert(ignore_permissions=True)
            
            # If no exception is raised, fail the test
            self.fail(f"Duplicate alert insertion did not raise an exception for {email} in {region}")
        except frappe.exceptions.ValidationError as e:
            self.assertEqual(str(e), "Alert already registered for this email and region.")
            print(f"Duplicate alert check passed: {email} already registered for {region}")
