# Copyright (c) 2026, Mahmoud Khaled and contributors
# For license information, please see license.txt

from frappe.model.document import Document


class FlightPassenger(Document):

    def validate(self):
        first_name = (self.first_name or "").strip()
        last_name = (self.last_name or "").strip()

        self.full_name = f"{first_name} {last_name}".strip()
