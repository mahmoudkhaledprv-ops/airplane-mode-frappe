# Copyright (c) 2026, Mahmoud Khaled and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import today


class RentPayment(Document):

    def validate(self):
        if self.status == "Paid":
            if not self.payment_date:
                self.payment_date = today()

            if not self.receipt_number:
                self.receipt_number = frappe.generate_hash(length=12).upper()

        else:
            self.receipt_number = None