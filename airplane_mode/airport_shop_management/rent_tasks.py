import calendar

import frappe
from frappe.utils import flt, get_first_day, getdate, nowdate


def generate_monthly_rent():
    """Create one unpaid rent payment per occupied shop per month."""

    today = getdate(nowdate())
    month_start = get_first_day(today)
    month_end = getdate(
        f"{today.year}-{today.month:02d}-"
        f"{calendar.monthrange(today.year, today.month)[1]:02d}"
    )

    default_rent = flt(
        frappe.db.get_single_value(
            "Shop Rent Settings", "default_rent_amount"
        )
    )

    shops = frappe.get_all(
        "Airport Shop",
        filters={"status": "Occupied"},
        fields=[
            "name",
            "tenant",
            "rent_amount",
            "contract_start_date",
            "contract_expiry_date",
        ],
    )

    created = 0

    for shop in shops:
        if not shop.tenant:
            continue

        if (
            shop.contract_start_date
            and getdate(shop.contract_start_date) > month_end
        ):
            continue

        if (
            shop.contract_expiry_date
            and getdate(shop.contract_expiry_date) < month_start
        ):
            continue

        # Avoid duplicate payments for the same shop and month.
        if frappe.db.exists(
            "Rent Payment",
            {
                "shop": shop.name,
                "payment_month": month_start,
                "docstatus": ["<", 2],
            },
        ):
            continue

        amount = flt(shop.rent_amount) or default_rent

        if amount <= 0:
            frappe.log_error(
                title="Monthly Rent: Invalid Amount",
                message=f"Shop {shop.name} has no valid rent amount.",
            )
            continue

        payment = frappe.get_doc({
            "doctype": "Rent Payment",
            "shop": shop.name,
            "tenant": shop.tenant,
            "payment_month": month_start,
            "due_date": getdate(
                f"{today.year}-{today.month:02d}-10"
            ),
            "amount": amount,
            "status": "Unpaid",
        })

        payment.insert(ignore_permissions=True)
        created += 1

    frappe.logger().info(
        f"Monthly rent generation completed: {created} payments created."
    )

    return created
