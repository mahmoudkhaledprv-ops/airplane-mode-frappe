import random

import frappe


def execute():
    tickets = frappe.get_all(
        "Airplane Ticket",
        filters={"seat": ["in", ["", None]]},
        pluck="name",
    )

    for ticket_name in tickets:
        seat_number = random.randint(1, 99)
        seat_letter = random.choice("ABCDE")

        seat = f"{seat_number}{seat_letter}"

        frappe.db.set_value(
            "Airplane Ticket",
            ticket_name,
            "seat",
            seat,
            update_modified=False,
        )
