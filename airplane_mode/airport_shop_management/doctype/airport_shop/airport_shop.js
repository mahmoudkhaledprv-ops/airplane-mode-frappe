// Copyright (c) 2026, Mahmoud Khaled and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airport Shop", {
    setup(frm) {
        frm.set_query("shop_type", () => {
            return {
                filters: {
                    enabled: 1
                }
            };
        });
    }
});