// Copyright (c) 2026, Mahmoud Khaled and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airplane Ticket", {
    refresh(frm) {
        if (frm.is_new() || frm.doc.docstatus !== 0) {
            return;
        }

        frm.add_custom_button(__("Assign Seat"), () => {
            const dialog = new frappe.ui.Dialog({
                title: __("Select Seat"),
                fields: [
                    {
                        label: __("Seat Number"),
                        fieldname: "seat_number",
                        fieldtype: "Data",
                        reqd: 1,
                        default: frm.doc.seat || ""
                    }
                ],
                primary_action_label: __("Assign"),
                primary_action: async (values) => {
                    const seat = values.seat_number.trim().toUpperCase();

                    if (!/^(?:[1-9]|[1-9][0-9])[A-E]$/.test(seat)) {
                        frappe.msgprint(
                            __("Enter a valid seat, such as 12A or 51D.")
                        );
                        return;
                    }

                    try {
                        await frm.set_value("seat", seat);
                        await frm.save();

                        dialog.hide();

                        frappe.show_alert({
                            message: __("Seat assigned successfully"),
                            indicator: "green"
                        });
                    } catch (error) {
                        console.error("Seat assignment failed:", error);
                    }
                }
            });

            dialog.show();
        });
    }
});