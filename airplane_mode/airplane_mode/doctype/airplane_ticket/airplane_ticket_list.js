frappe.listview_settings["Airplane Ticket"] = {
    add_fields: ["status"],

    has_indicator_for_draft: true,
    has_indicator_for_cancelled: true,

    get_indicator: function (doc) {
        const colors = {
            "Booked": "gray",
            "Checked-In": "purple",
            "Boarded": "green"
        };

        const color = colors[doc.status] || "gray";

        return [
            __(doc.status || "Booked"),
            color,
            "status,=," + (doc.status || "Booked")
        ];
    }
};
