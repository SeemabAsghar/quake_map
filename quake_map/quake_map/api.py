import frappe, requests, json
from datetime import datetime, timedelta


USGS_API_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"


def fetch_earthquake_data():
    now = datetime.now()
    params = {
        "format": "geojson",
        "starttime": (now - timedelta(days=15)).isoformat(),
        "endtime": now.isoformat(),
    }
    response = requests.get(USGS_API_URL, params=params)
    response.raise_for_status()
    return response.json().get("features", [])


def save_to_frappe(event):
    properties = event["properties"]
    geometry = event["geometry"]["coordinates"]
    coordinates = json.dumps({
        "latitude": geometry[1],
        "longitude": geometry[0]
    })
    
    if not frappe.db.exists("Earthquake Data", {"id": event["id"]}):
        doc = frappe.get_doc({
            "doctype": "Earthquake Data",
            "id": event["id"],
            "magnitude": properties.get("mag"),
            "place": properties.get("place"),
            "latitude": geometry[1],
            "longitude": geometry[0],
            "depth": geometry[2],
            "significance": properties.get("sig"),
            "time": datetime.fromtimestamp(properties.get("time") / 1000),
            "coordinates": coordinates
        })
        existing_doc = frappe.db.exists("Earthquake Data", {"id": event["id"]})
        if existing_doc:
            doc.name = existing_doc
            doc.save()
        else:
            doc.insert()
            doc.save()

def fetch_and_store_earthquake_data():
    data = fetch_earthquake_data()
    for event in data:
            save_to_frappe(event)

    frappe.db.commit()
    final_count = frappe.db.count("Earthquake Data")
    print(f"Final record count: {final_count}")