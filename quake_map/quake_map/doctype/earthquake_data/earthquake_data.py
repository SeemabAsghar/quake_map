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

        self.alert_level = self.classify_earthquake()
        affected_users = frappe.db.sql(
        """
            SELECT email FROM `tabAlerts`
            WHERE region LIKE %s
        """, 
        (f"%{self.place.split(',')[-1].strip()}%",), as_dict=True)

        for user in affected_users:
           frappe.sendmail(
            recipients=user.email,
            subject=_("🌍 Earthquake Alert: {0} Earthquake Detected").format(self.alert_level),
            message=_(""" 
            <div style="font-family: 'Georgia', sans-serif; color: #333; line-height: 1.8; padding: 20px; border: 1px solid #ddd; border-radius: 8px; max-width: 600px; margin: 20px auto; box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);">
                <h2 style="color: #D9534F; text-align: center;">⚠️ {0} Earthquake Alert</h2>
                <div style="margin: 20px 0;">
                    <p><strong>🌡 Magnitude:</strong> <span style="color: #D9534F;">{1}</span></p>
                    <p><strong>📍 Location:</strong> {2}</p>
                    <p><strong>🕒 Time:</strong> {3}</p>
                    <p><strong>🌐 Coordinates:</strong> {4}, {5}</p>
                </div>
                <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
                <div style="background-color: #fef3c7; padding: 15px; border-radius: 5px;">
                    <h3 style="color: #D97706;">🔹 What You Should Know</h3>
                    <p>Earthquakes can cause damage to buildings and infrastructure. Aftershocks may follow the initial quake. Stay alert and prepared.</p>
                    <p><strong>Precautionary Measures:</strong></p>
                    <ul style="padding-left: 20px;">
                        <li>🏠 Move to an open area away from buildings and power lines if possible.</li>
                        <li>🛡️ Drop, cover, and hold on if indoors. Protect your head and neck.</li>
                        <li>🚪 Stand in a doorway or take shelter under sturdy furniture.</li>
                        <li>📱 Stay informed through local authorities and alerts.</li>
                    </ul>
                </div>
                <p style="margin-top: 30px; text-align: center; color: #888;">Your safety is our top priority. Please take care and remain vigilant.</p>
            </div>
            """).format(self.alert_level, self.magnitude, self.place, self.time, self.latitude, self.longitude)
            )

        frappe.msgprint("Alert sent for earthquake at {0}".format(self.place))


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
        filters.append=_("%, {0},%").format(city)
    
    query_response = frappe.db.sql(
        _("""
        SELECT * FROM `tabEarthquake Data`
        {0}
        """).
        format(conditions),
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
