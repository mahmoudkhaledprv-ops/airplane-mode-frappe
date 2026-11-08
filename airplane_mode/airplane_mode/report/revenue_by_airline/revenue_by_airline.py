import frappe
from frappe.utils import flt


def execute(filters=None):
    columns = [
        {
            "label": "Airline",
            "fieldname": "airline",
            "fieldtype": "Link",
            "options": "Airline",
            "width": 220,
        },
        {
            "label": "Revenue",
            "fieldname": "revenue",
            "fieldtype": "Currency",
            "width": 180,
        },
    ]

    # Include all airlines, even those with no revenue.
    airlines = frappe.get_all("Airline", pluck="name")
    revenue_by_airline = {airline: 0.0 for airline in airlines}

    airplanes = frappe.get_all(
        "Airplane",
        fields=["name", "airline"],
    )
    airplane_to_airline = {
        row.name: row.airline for row in airplanes
    }

    flights = frappe.get_all(
        "Airplane Flight",
        fields=["name", "airplane"],
    )
    flight_to_airline = {
        row.name: airplane_to_airline.get(row.airplane)
        for row in flights
    }

    # Only submitted tickets count as revenue.
    tickets = frappe.get_all(
        "Airplane Ticket",
        filters={"docstatus": 1},
        fields=["flight", "total_amount"],
    )

    for ticket in tickets:
        airline = flight_to_airline.get(ticket.flight)
        if airline in revenue_by_airline:
            revenue_by_airline[airline] += flt(ticket.total_amount)

    data = [
        {
            "airline": airline,
            "revenue": revenue,
        }
        for airline, revenue in revenue_by_airline.items()
    ]

    data.sort(key=lambda row: row["revenue"], reverse=True)

    total_revenue = sum(row["revenue"] for row in data)

    chart = {
        "data": {
            "labels": [row["airline"] for row in data],
            "datasets": [{
                "name": "Revenue",
                "values": [row["revenue"] for row in data],
            }],
        },
        "type": "donut",
        "height": 300,
    }

    report_summary = [{
        "label": "Total Revenue",
        "value": total_revenue,
        "indicator": "Green",
        "datatype": "Currency",
    }]

    return columns, data, None, chart, report_summary
