# Copyright (c) 2026, Mahmoud Khaled and Contributors
# See license.txt

import frappe
from frappe.tests import IntegrationTestCase


class IntegrationTestAirportShop(IntegrationTestCase):
    """Integration tests for Airport Shop validation."""

    def setUp(self):
        super().setUp()

        airport_code = f"T{frappe.generate_hash(length=7).upper()}"

        airport = frappe.get_doc({
            "doctype": "Airport",
            "name": airport_code,
            "__newname": airport_code,
            "code": airport_code,
            "city": "Test City",
            "country": "Test Country",
        })

        airport.insert()
        self.airport = airport.name

    def make_shop(self, **overrides):
        data = {
            "doctype": "Airport Shop",
            "shop_number": frappe.generate_hash(length=10),
            "shop_name": "Automated Test Shop",
            "airport": self.airport,
            "area": 50,
            "rent_amount": 5000,
            "status": "Available",
            "is_published": 0,
        }

        data.update(overrides)
        return frappe.get_doc(data)

    def test_valid_shop(self):
        shop = self.make_shop()
        shop.insert()

        self.assertTrue(shop.name)
        self.assertEqual(shop.status, "Available")

    def test_area_must_be_positive(self):
        for area in (0, -10):
            with self.subTest(area=area):
                shop = self.make_shop(area=area)

                with self.assertRaises(frappe.ValidationError):
                    shop.insert()

    def test_rent_cannot_be_negative(self):
        shop = self.make_shop(rent_amount=-100)

        with self.assertRaises(frappe.ValidationError):
            shop.insert()

    def test_contract_dates_must_be_valid(self):
        shop = self.make_shop(
            contract_start_date="2027-12-31",
            contract_expiry_date="2027-01-01",
        )

        with self.assertRaises(frappe.ValidationError):
            shop.insert()

    def test_occupied_shop_requires_tenant(self):
        shop = self.make_shop(
            status="Occupied",
            tenant=None,
        )

        with self.assertRaises(frappe.ValidationError):
            shop.insert()