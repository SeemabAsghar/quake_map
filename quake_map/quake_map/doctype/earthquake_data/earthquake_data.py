# Copyright (c) 2024, Seemab and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from datetime import datetime
from frappe.model.document import Document


class EarthquakeData(Document):
	def after_insert(self):
        self.send_alerts()

    def send_alerts(self):
        if self.magnitude < 3.0:
            return  

        alert_level = self.classify_earthquake(self)
        affected_users = frappe.db.sql(
        """
            SELECT email FROM `tabAlerts`
            WHERE region LIKE %s
        """, 
        (f"%{self.place.split(',')[-1].strip()}%",), as_dict=True)

        for user in affected_users:
            frappe.sendmail(
                recipients=user.email,
                subject= _("Earthquake Alert: {0} Earthquake Detected").format(alert_level),
                message=f"""
                A {alert_level} earthquake of magnitude {self.magnitude} was detected at {self.place}.
                Time: {self.time}
                Latitude: {self.latitude}, Longitude: {self.longitude}.
                Stay safe and take necessary precautions.
                """
            )
        
        frappe.msgprint(f"Alert sent for earthquake at {self.place}")


    def classify_earthquake(self):
        
        if 3.0 <= self.magnitude <= 3.9:
            return "Minor Earthquake."
        elif 4.0 <= self.magnitude <= 4.9:
            return "Light Earthquake."
        elif 5.0 <= self.magnitude <= 5.9:
            return "Moderate Earthquake."
        elif 6.0 <= self.magnitude <= 6.9:
            return "Strong Earthquake."
        elif 7.0 <= self.magnitude <= 7.9:
            return "Major Earthquake."
        elif 8.0 <= self.magnitude <= 8.9:
            return " Great Earthquake."
        elif self.magnitude >= 9.0:
            return "Mega-Earthquake."
        else:
            return "Unknown Earthquake."


@frappe.whitelist()
def fetch_data(start_date, end_date, min_magnitude=None, max_magnitude=None, city=None):

    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    
    conditions = "WHERE DATE(time) BETWEEN %s AND %s"
    filters = [start_date, end_date]
    
    if min_magnitude is not None and min_magnitude.strip():
        conditions += " AND magnitude >= %s"
        filters.append(float(min_magnitude))
    
    if max_magnitude is not None and max_magnitude.strip():
        conditions += " AND magnitude <= %s"
        filters.append(float(max_magnitude))
    
    if city:
        conditions += " AND place LIKE %s"
        filters.append(f"%, {city}")
    
    query_response = frappe.db.sql(
        f"""
        SELECT * FROM `tabEarthquake Data`
        {conditions}
        """,
        tuple(filters),
        as_dict=True,
    )
    return query_response


@frappe.whitelist()
def get_cities():
    places = frappe.db.sql(
        """
        SELECT DISTINCT place
        FROM `tabEarthquake Data`
        """,
        as_list=True,
    )
    
    cities = set()
    for place in places:
        if place[0] and ',' in place[0]:
            city = place[0].split(",")[-1].strip()
            cities.add(city)
        elif place[0]:
            cities.add(place[0].strip())
    
    sorted_cities = sorted(list(cities))    
    return sorted_cities
