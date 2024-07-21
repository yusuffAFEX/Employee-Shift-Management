// Copyright (c) 2024, Yusuff and contributors
// For license information, please see license.txt

frappe.query_reports["Employee Shift Report"] = {
	"filters": [
			{
            "fieldname": "start_date",
            "label": __("Start Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.month_start()
        },
        {
            "fieldname": "end_date",
            "label": __("End Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.month_end()
        }
	],
	onload: function(report) {
        report.page.add_inner_button(__('Send Report via Email'), function() {
            frappe.prompt({
                label: 'Email Address',
                fieldname: 'email',
                fieldtype: 'Data',
                reqd: 1
            }, function(values){
                const email = values.email;
                const filters = report.get_values();
                frappe.call({
                    method: 'employee_shift.employee_shift.report.employee_shift_report.employee_shift_report.send_report_via_email',
                    args: {
                        email: email,
                        filters: filters
                    },
                    callback: function(response) {
                        if (response.message === 'success') {
                            frappe.msgprint(__('Email sent successfully!'));
                        } else {
                            frappe.msgprint(__('There was an issue sending the email.'));
                        }
                    }
                });
            }, __('Enter Email Address'), __('Send'));
        });
    }
};
