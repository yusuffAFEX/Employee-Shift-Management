frappe.listview_settings['Employee'] = {
    onload: function(listview) {
        listview.page.add_inner_button(__('Create Shift'), function() {
            const selected_docs = listview.get_checked_items();
				console.log(selected_docs)
            if (selected_docs.length === 0) {
                frappe.msgprint(__('Please select at least one document.'));
                return;
            }

			console.log('selected_docs', selected_docs)

            // Open a new dialog to take additional information
            const d = new frappe.ui.Dialog({
                title: __('Other Information'),
                fields: [
                    {
                        label: __('Location'),
                        fieldname: 'location',
                        fieldtype: 'Link',
                        options: 'Location',
                        reqd: 1
                    },
                    {
                        label: __('Date'),
                        fieldname: 'date',
                        fieldtype: 'Date',
                        reqd: 1
                    },
					{
                        label: __('From Time'),
                        fieldname: 'from_time',
                        fieldtype: 'Time',
                        reqd: 1
                    },
					{
                        label: __('To Time'),
                        fieldname: 'to_time',
                        fieldtype: 'Time',
                        reqd: 1
                    }
                ],
                primary_action_label: __('Submit'),
                primary_action(values) {

					const today = new Date();
                    const shiftDate = new Date(values.date);

                    // Validate shift start date
                    if (shiftDate <= today) {
                        frappe.msgprint(__('Shift date has to be greater than today.'));
                        return;
                    }

					// if (shiftDate === today) {
					// 	const fromTimeParts = values.from_time.split(':');
                    //     const fromTime = new Date();
                    //     fromTime.setHours(fromTimeParts[0], fromTimeParts[1], fromTimeParts[2]);
					//
                    //     if (fromTime < currentTime) {
                    //         frappe.msgprint(__('From time is in the past.'));
                    //         return;
                    //     }
                    // }


                    d.hide();
                    frappe.call({
                        method: 'employee_shift.employee_shift.doctype.employee_shift.employee_shift.process_selected_docs',
                        args: {
                            docs: selected_docs.map(doc => doc.name),
                            additional_data: values
                        },
                        callback: function(r) {
                            if (r.message) {
                                frappe.msgprint(__('Employee shifts created successfully.'));
                                listview.refresh();
                            }
                        }
                    });
                }
            });

            d.show();
        });
    }
};
