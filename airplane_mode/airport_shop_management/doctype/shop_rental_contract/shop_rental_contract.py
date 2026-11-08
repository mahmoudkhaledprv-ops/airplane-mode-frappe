# Copyright (c) 2026, Mahmoud Khaled and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt, getdate

from airplane_mode.airport_shop_management.shop_occupancy import (
    sync_shop_occupancy,
)


class ShopRentalContract(Document):
    def validate(self):
        self.validate_contract_dates()
        self.validate_monthly_rent()

    def before_submit(self):
        self.validate_overlapping_contracts()

    def on_submit(self):
        sync_shop_occupancy(self.shop)

    def on_cancel(self):
        sync_shop_occupancy(self.shop)

    def validate_contract_dates(self):
        if not self.start_date or not self.end_date:
            return

        if getdate(self.end_date) < getdate(self.start_date):
            frappe.throw(
                _("Contract End Date cannot be before Start Date."),
                title=_("Invalid Contract Dates"),
            )

    def validate_monthly_rent(self):
        if flt(self.monthly_rent) <= 0:
            frappe.throw(
                _("Monthly Rent must be greater than zero."),
                title=_("Invalid Monthly Rent"),
            )

    def validate_overlapping_contracts(self):
        if not self.shop or not self.start_date or not self.end_date:
            return

        overlapping_contracts = frappe.get_all(
            "Shop Rental Contract",
            filters={
                "shop": self.shop,
                "docstatus": 1,
                "name": ["!=", self.name],
                "start_date": ["<=", self.end_date],
                "end_date": [">=", self.start_date],
            },
            fields=["name"],
            limit_page_length=1,
        )

        if overlapping_contracts:
            existing_contract = overlapping_contracts[0].name

            frappe.throw(
                _(
                    "Shop {0} already has an approved contract "
                    "({1}) overlapping this rental period."
                ).format(
                    frappe.bold(self.shop),
                    frappe.bold(existing_contract),
                ),
                title=_("Overlapping Rental Contract"),
            )