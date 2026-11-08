# Copyright (c) 2026, Mahmoud Khaled and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import getdate, today


def sync_shop_occupancy(shop_name):
    """
    Synchronize shop occupancy based on submitted rental contracts.

    Rules:
    - A currently active, submitted contract makes the shop Occupied.
    - Future contracts do not occupy the shop before their start date.
    - Cancelled contracts do not count as active contracts.
    - Shops with no rental contract history can retain legacy contracts.
    """

    if not frappe.db.exists("Airport Shop", shop_name):
        return

    current_date = getdate(today())

    # Find a submitted contract that is active today.
    active_contracts = frappe.get_all(
        "Shop Rental Contract",
        filters={
            "shop": shop_name,
            "docstatus": 1,
            "status": "Active",
            "start_date": ["<=", current_date],
            "end_date": [">=", current_date],
        },
        fields=[
            "name",
            "tenant",
            "start_date",
            "end_date",
            "monthly_rent",
        ],
        order_by="start_date desc",
        limit=1,
    )

    if active_contracts:
        contract = active_contracts[0]

        frappe.db.set_value(
            "Airport Shop",
            shop_name,
            {
                "status": "Occupied",
                "tenant": contract.tenant,
                "contract_start_date": contract.start_date,
                "contract_expiry_date": contract.end_date,
                "rent_amount": contract.monthly_rent,
            },
        )
        return

    # If the shop has ever used the new contract system,
    # those contracts are the source of truth.
    has_contract_history = frappe.db.exists(
        "Shop Rental Contract",
        {"shop": shop_name},
    )

    if has_contract_history:
        frappe.db.set_value(
            "Airport Shop",
            shop_name,
            {
                "status": "Available",
                "tenant": None,
                "contract_start_date": None,
                "contract_expiry_date": None,
            },
        )
        return

    # Backward compatibility for shops using legacy contract fields.
    shop = frappe.db.get_value(
        "Airport Shop",
        shop_name,
        [
            "tenant",
            "contract_start_date",
            "contract_expiry_date",
        ],
        as_dict=True,
    )

    if (
        shop.tenant
        and shop.contract_start_date
        and shop.contract_expiry_date
        and getdate(shop.contract_start_date) <= current_date
        <= getdate(shop.contract_expiry_date)
    ):
        frappe.db.set_value(
            "Airport Shop",
            shop_name,
            "status",
            "Occupied",
        )
        return

    # No currently valid rental contract.
    frappe.db.set_value(
        "Airport Shop",
        shop_name,
        {
            "status": "Available",
            "tenant": None,
            "contract_start_date": None,
            "contract_expiry_date": None,
        },
    )


def sync_all_shops():
    """
    Daily job to synchronize all shops managed by rental contracts.

    Includes submitted and cancelled contracts so that
    occupancy remains correct after cancellations.
    """

    contracts = frappe.get_all(
        "Shop Rental Contract",
        filters={"docstatus": ["in", [1, 2]]},
        pluck="shop",
    )

    shop_names = sorted(set(contracts))

    for shop_name in shop_names:
        sync_shop_occupancy(shop_name)

    return {
        "shops_processed": len(shop_names),
        "status": "completed",
    }