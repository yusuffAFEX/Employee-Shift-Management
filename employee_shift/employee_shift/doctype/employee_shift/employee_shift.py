# Copyright (c) 2024, Yusuff and contributors
# For license information, please see license.txt
import csv
import json
from datetime import date, datetime

import frappe
# import frappe
from frappe.model.document import Document
from io import StringIO
from frappe import _


class EmployeeShift(Document):

	def before_submit(self):
		todays_date = date.today()
		current_time = datetime.now().time()

		# Convert self.date to a datetime.date object
		try:
			shift_date = datetime.strptime(self.date, '%Y-%m-%d').date()
		except ValueError:
			frappe.throw("Date format should be YYYY-MM-DD")

		if shift_date < todays_date:
			frappe.throw("Date has to be greater than today")

		if shift_date == todays_date:
			try:
				from_time = datetime.strptime(self.from_time, '%H:%M:%S').time()
			except ValueError:
				frappe.throw("Time format should be HH:MM:SS")

			if from_time < current_time:
				frappe.throw("From time is in the past")


@frappe.whitelist()
def process_selected_docs(docs, additional_data):
	docs = json.loads(docs)
	additional_data = json.loads(additional_data)
	location = additional_data.get('location')
	date = additional_data.get('date')
	from_time = additional_data.get('from_time')
	to_time = additional_data.get('to_time')

	print('docs', docs)

	for doc_name in docs:
		doc = frappe.get_doc('Employee', doc_name)
		print('doc', doc.as_dict())
		employee_shift = frappe.get_doc({
			'doctype': 'Employee Shift',
			'employee': doc_name,
			'date': date,
			'location': location,
			'from_time': from_time,
			'to_time': to_time,
		})
		print('New Employee Shift:', employee_shift.as_dict())
		employee_shift.insert()
		employee_shift.submit()

	return True


def generate_and_send_report(email):
	today = frappe.utils.nowdate()  # Get today's date
	filters = {
		'date': today,
	}

	# Function to get columns
	def get_columns():
		return [
			{"label": _("Employee ID"), "fieldname": "employee_id", "fieldtype": "Data"},
			{"label": _("Employee Name"), "fieldname": "employee_name", "fieldtype": "Data"},
			{"label": _("Location"), "fieldname": "location", "fieldtype": "Data"},
			{"label": _("Date"), "fieldname": "date", "fieldtype": "Date"},
			{"label": _("From Time"), "fieldname": "from_time", "fieldtype": "Time"},
			{"label": _("To Time"), "fieldname": "to_time", "fieldtype": "Time"},
			{"label": _("Department"), "fieldname": "department", "fieldtype": "Data"},
		]

	# Function to get data
	def get_data(filters):
		return frappe.db.get_list(
			'Employee Shift',
			fields=['employee_id', 'employee_name', 'location', 'date', 'from_time', 'to_time',
					'department'],
			filters=filters,
			order_by='date'
		)

	# Execute the report generation
	columns = get_columns()
	data = get_data(filters)

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
		subject=_("Employee Shift Report for Today"),
		message=_("Please find attached the Employee Shift Report for today."),
		attachments=[{
			'fname': 'employee_shift_report.csv',
			'fcontent': csv_content
		}]
	)

	return 'success'


def generate_and_send_report_task():
	email = "yusufoyedele43@gmail.com"
	generate_and_send_report(email)
