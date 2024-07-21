// Copyright (c) 2024, Yusuff and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Employee", {
// 	refresh(frm) {

// 	},
// });

frappe.ui.form.on('Employee', {
    refresh: function(frm) {
        frm.add_custom_button('Schedule Shift', () => {
            frappe.new_doc('Employee Shift', {
                employee: frm.doc.name
            })
        })
    }
});


