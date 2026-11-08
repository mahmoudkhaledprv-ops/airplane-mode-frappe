# Copyright (c) 2026, Mahmoud Khaled and contributors
# For license information, please see license.txt

import random

import frappe
from frappe.model.document import Document
from frappe.utils import flt


class AirplaneTicket(Document):

    def before_insert(self):
        self.validate_flight_capacity()
        self.assign_seat()

    def validate_flight_capacity(self):
        if not self.flight:
            return

        airplane = frappe.db.get_value(
            "Airplane Flight",
            self.flight,
            "airplane",
        )

        if not airplane:
            frappe.throw("Please select a valid Airplane Flight.")

        capacity = frappe.db.get_value(
            "Airplane",
            airplane,
            "capacity",
        )

        if capacity is None:
            frappe.throw("Airplane capacity is not configured.")

        capacity = int(capacity)

        ticket_count = frappe.db.count(
            "Airplane Ticket",
            filters={"flight": self.flight},
        )

        if ticket_count >= capacity:
            frappe.throw(
                f"Cannot create ticket. Flight capacity of {capacity} "
                "passengers has been reached."
            )

    def validate(self):
        self.remove_duplicate_addons()
        self.calculate_total_amount()

    def assign_seat(self):
        seat_number = random.randint(1, 99)
        seat_letter = random.choice("ABCDE")

        self.seat = f"{seat_number}{seat_letter}"

    def remove_duplicate_addons(self):
        seen_items = set()
        unique_addons = []

        for addon in self.get("add_ons") or []:
            if addon.item in seen_items:
                continue

            seen_items.add(addon.item)
            unique_addons.append(addon)

        self.set("add_ons", unique_addons)

    def calculate_total_amount(self):
        total = flt(self.flight_price)

        for addon in self.get("add_ons") or []:
            total += flt(addon.amount)

        self.total_amount = total

    def before_submit(self):
        if self.status != "Boarded":
            frappe.throw(
                "Only tickets with status Boarded can be submitted."
            )