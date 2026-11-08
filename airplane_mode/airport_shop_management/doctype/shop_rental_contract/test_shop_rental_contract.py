# Copyright (c) 2026, Mahmoud Khaled and Contributors
# See license.txt

import frappe
from frappe.tests import IntegrationTestCase
from frappe.utils import add_days, today


class IntegrationTestShopRentalContract(IntegrationTestCase):
    """Integration tests for rental contract business logic."""

    def setUp(self):
        super().setUp()

        unique_id = frappe.generate_hash(length=8).upper()

        # Create an independent test airport.
        airport = frappe.get_doc({
            "doctype": "Airport",
            "name": f"TEST-{unique_id}",
            "__newname": f"TEST-{unique_id}",
            "code": f"T{unique_id}",
            "city": "Test City",
            "country": "Test Country",
        })
        airport.insert()
        self.airport = airport.name

        # Create an available shop.
        shop = frappe.get_doc({
            "doctype": "Airport Shop",
            "shop_number": f"SHOP-{unique_id}",
            "shop_name": f"Test Rental Shop {unique_id}",
            "airport": self.airport,
            "area": 50,
            "rent_amount": 5000,
            "status": "Available",
            "is_published": 0,
        })
        shop.insert()
        self.shop = shop.name

        # Create a tenant linked to that shop.
        tenant = frappe.get_doc({
            "doctype": "Shop Tenant",
            "tenant_name": f"Test Tenant {unique_id}",
            "shop": self.shop,
        })
        tenant.insert()
        self.tenant = tenant.name

    def make_contract(self, **overrides):
        """Build a rental contract with valid default data."""

        data = {
            "doctype": "Shop Rental Contract",
            "shop": self.shop,
            "tenant": self.tenant,
            "start_date": add_days(today(), 30),
            "end_date": add_days(today(), 60),
            "monthly_rent": 5000,
            "status": "Active",
        }

        data.update(overrides)

        return frappe.get_doc(data)

    def test_valid_contract(self):
        contract = self.make_contract()
        contract.insert()

        self.assertTrue(contract.name)
        self.assertEqual(contract.docstatus, 0)

    def test_invalid_contract_dates(self):
        contract = self.make_contract(
            start_date="2027-12-31",
            end_date="2027-01-01",
        )

        with self.assertRaises(frappe.ValidationError):
            contract.insert()

    def test_monthly_rent_must_be_positive(self):
        for amount in (0, -500):
            with self.subTest(amount=amount):
                contract = self.make_contract(
                    monthly_rent=amount
                )

                with self.assertRaises(frappe.ValidationError):
                    contract.insert()

    def test_overlapping_contracts_are_blocked(self):
        # Approve the first contract.
        first = self.make_contract()
        first.insert()
        first.submit()

        self.assertEqual(first.docstatus, 1)

        # The second contract overlaps the first.
        second = self.make_contract(
            start_date=add_days(today(), 45),
            end_date=add_days(today(), 75),
        )
        second.insert()

        with self.assertRaises(frappe.ValidationError):
            second.submit()

        saved_docstatus = frappe.db.get_value(
            "Shop Rental Contract", second.name, "docstatus"
        )
        self.assertEqual(saved_docstatus, 0)

    def test_active_contract_updates_shop(self):
        # Create a contract that is valid today.
        contract = self.make_contract(
            start_date=today(),
            end_date=add_days(today(), 30),
        )

        contract.insert()
        contract.submit()

        # Verify that the contract updated the shop.
        shop_status = frappe.db.get_value(
            "Airport Shop",
            self.shop,
            "status",
        )

        shop_tenant = frappe.db.get_value(
            "Airport Shop",
            self.shop,
            "tenant",
        )

        self.assertEqual(shop_status, "Occupied")
        self.assertEqual(shop_tenant, self.tenant)

    def test_cancel_active_contract_releases_shop(self):
        contract = self.make_contract(
            start_date=today(),
            end_date=add_days(today(), 30),
        )

        contract.insert()
        contract.submit()

        self.assertEqual(
            frappe.db.get_value("Airport Shop", self.shop, "status"),
            "Occupied",
        )

        contract.cancel()

        self.assertEqual(
            frappe.db.get_value("Airport Shop", self.shop, "status"),
            "Available",
        )

        self.assertFalse(
            frappe.db.get_value("Airport Shop", self.shop, "tenant")
        )
