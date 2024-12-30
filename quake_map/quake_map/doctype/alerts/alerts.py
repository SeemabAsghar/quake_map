import frappe
from frappe.model.document import Document


class Alerts(Document):
	pass

@frappe.whitelist()
def register_alert(email, region):
    if not frappe.db.exists("Alerts", {"email": email, "region": region}):
        frappe.get_doc({
            "doctype": "Alerts",
            "email": email,
            "region": region,
        }).insert()
        return "success"
    else:
        return "already_registered"

