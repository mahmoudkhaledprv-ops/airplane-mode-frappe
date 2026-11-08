import frappe


def get_context(context):
    context.title = "Airport Shops"
    context.no_cache = 1

    # Only expose public information about available shops.
    context.shops = frappe.get_all(
        "Airport Shop",
        filters={
            "status": "Available",
            "is_published": 1,
        },
        fields=[
            "name",
            "shop_name",
            "airport",
            "shop_type",
            "area",
            "shop_location",
            "shop_description",
        ],
        order_by="shop_name asc",
    )
