# Copyright (c) 2024, Yusuff and contributors
# For license information, please see license.txt
import json
import csv
import frappe
from frappe import _
from io import StringIO


# import frappe


def execute(filters=None):
	columns, data = get_columns(), get_data(filters or {})
	return columns, data


def get_data(filters):
	conditions = []
	if filters.get("start_date"):
		conditions.append(["date", ">=", filters.get("start_date")])
	if filters.get("end_date"):
		conditions.append(["date", "<=", filters.get("end_date")])

	return frappe.db.get_list(
		'Employee Shift',
		fields=['employee_id', 'employee_name', 'location', 'date', 'from_time', 'to_time',
				'department'],
		filters=conditions,
		order_by='date'
	)

def get_columns():
	return [
		{
			"label": _("Employee ID"),
			"fieldname": "employee_id",
			"fieldtype": "Data",
			"width": 150
		},
		{
			"label": _("Employee Name"),
			"fieldname": "employee_name",
			"fieldtype": "Data",
			"width": 150
		},
		{
			"label": _("Location"),
			"fieldname": "location",
			"fieldtype": "Data",
			"width": 150
		},
		{
			"label": _("Date"),
			"fieldname": "date",
			"fieldtype": "Date",
			"width": 150
		},
		{
			"label": _("From Time"),
			"fieldname": "from_time",
			"fieldtype": "Time",
			"width": 150
		},
		{
			"label": _("To Time"),
			"fieldname": "to_time",
			"fieldtype": "Time",
			"width": 150
		},
		{
			"label": _("Department"),
			"fieldname": "department",
			"fieldtype": "Data",
			"width": 150
		},
	]


@frappe.whitelist()
def send_report_via_email(email, filters):
	if isinstance(filters, str):
		filters = json.loads(filters)
	print('filter', filters)
	print('email', email)
	print('filter type', type(filters))
	columns, data = execute(filters)

	# Convert data to CSV
	csv_file = StringIO()
	csv_writer = csv.writer(csv_file)

	# Write the header
	header = [col['label'] for col in columns]
	csv_writer.writerow(header)

	# Write the data
	for row in data:
		csv_writer.writerow([row[col['fieldname']] for col in columns])

	# Get CSV content
	csv_content = csv_file.getvalue()
	csv_file.close()

	# Send the email with CSV attachment
	frappe.sendmail(
		recipients=email,
		subject=_("Employee Shift Report"),
		message=_("Please find attached the Employee Shift Report."),
		attachments=[{
			'fname': 'employee_shift_report.csv',
			'fcontent': csv_content
		}]
	)
	print('got here')

	return 'success'
