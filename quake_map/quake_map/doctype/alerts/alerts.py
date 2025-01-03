import frappe
from frappe.model.document import Document



class Alerts(Document):
	def validate(self):
		if frappe.db.exists("Alerts", {"email": self.email, "region": self.region}):
			frappe.throw("Alert already registered for this email and region.")



@frappe.whitelist()
def register_alert(email, region):
    if frappe.db.exists("Alerts", {"email": email, "region": region}):
        return "already_registered"
    else:
        frappe.get_doc({
            "doctype": "Alerts",
            "email": email,
            "region": region,
        }).insert()
        return "success"
