# Copyright (c) 2026, Mahmoud Khaled and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator


class AirplaneFlight(WebsiteGenerator):

    def before_submit(self):
        self.status = "Completed"

    def on_update(self):
        super().on_update()

        old_doc = self.get_doc_before_save()

        if old_doc and old_doc.gate_number != self.gate_number:
            frappe.enqueue(
                update_ticket_gates,
                queue="short",
                enqueue_after_commit=True,
                flight_name=self.name,
                gate_number=self.gate_number,
            )


def update_ticket_gates(flight_name, gate_number):
    # Ignore an outdated job if the flight gate changed again.
    current_gate = frappe.db.get_value(
        "Airplane Flight", flight_name, "gate_number"
    )

    if current_gate != gate_number:
        return

    tickets = frappe.get_all(
        "Airplane Ticket",
        filters={"flight": flight_name},
        pluck="name",
    )

    for ticket_name in tickets:
        frappe.db.set_value(
            "Airplane Ticket",
            ticket_name,
            "gate_number",
            gate_number,
            update_modified=False,
        )