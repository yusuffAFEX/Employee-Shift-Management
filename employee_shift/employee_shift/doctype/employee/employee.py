# Copyright (c) 2024, Yusuff and contributors
# For license information, please see license.txt
import uuid

from frappe.model.naming import make_autoname
# import frappe
from frappe.model.document import Document


class Employee(Document):

	def before_insert(self):
		self.employee_id = make_autoname('EMP-.#####')
