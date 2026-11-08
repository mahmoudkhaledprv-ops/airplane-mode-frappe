# Copyright (c) 2026, Mahmoud Khaled and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import flt, getdate
from frappe.website.website_generator import WebsiteGenerator


class AirportShop(WebsiteGenerator):

    def validate(self):
        self.validate_area()
        self.validate_rent_amount()
        self.validate_contract_dates()
        self.validate_occupancy()
        self.validate_tenant_assignment()

    def validate_area(self):
        if flt(self.area) <= 0:
            frappe.throw(
                _("Shop Area must be greater than zero."),
                title=_("Invalid Shop Area"),
            )

    def validate_rent_amount(self):
        if flt(self.rent_amount) < 0:
            frappe.throw(
                _("Rent Amount cannot be negative."),
                title=_("Invalid Rent Amount"),
            )

    def validate_contract_dates(self):
        if not self.contract_start_date or not self.contract_expiry_date:
            return

        if getdate(self.contract_expiry_date) < getdate(
            self.contract_start_date
        ):
            frappe.throw(
                _("Contract Expiry Date cannot be before Contract Start Date."),
                title=_("Invalid Contract Dates"),
            )

    def validate_occupancy(self):
        if self.status == "Occupied" and not self.tenant:
            frappe.throw(
                _("An occupied shop must have a tenant."),
                title=_("Tenant Required"),
            )

    def validate_tenant_assignment(self):
        if not self.tenant:
            return

        assigned_shop = frappe.db.get_value(
            "Shop Tenant",
            self.tenant,
            "shop",
        )

        if assigned_shop and assigned_shop != self.name:
            frappe.throw(
                _("Tenant {0} is already assigned to shop {1}.").format(
                    frappe.bold(self.tenant),
                    frappe.bold(assigned_shop),
                ),
                title=_("Tenant Assignment Conflict"),
            )