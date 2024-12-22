import frappe
from datetime import datetime

def get_context(context):
    pass


# @frappe.whitelist()
# def fetch_data(start_date, end_date):
#     start_date = datetime.strptime(start_date, "%Y-%m-%d")
#     end_date = datetime.strptime(end_date, "%Y-%m-%d")
#     query_response = frappe.db.sql(
#         """
#         SELECT * FROM `tabEarthquake Data`
#         WHERE DATE(time) BETWEEN %s AND %s
#         """,
#         (start_date, end_date),
#         as_dict=True,
#     )
#     return query_response
