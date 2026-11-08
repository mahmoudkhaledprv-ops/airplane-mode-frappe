# ✈️ Airplane Mode & Airport Shop Management

A custom Frappe Framework v16 application for managing airline operations and airport retail shops.

## 🚀 Features

### ✈️ Airline Management

- Airlines, airplanes, airports, and flights
- Flight crew management
- Passenger ticket management
- Automatic ticket gate updates using background jobs
- REST API integration

### 🏪 Airport Shop Management

- Airport shops and shop types
- Tenant management
- Rental contracts with overlapping-contract prevention
- Automatic shop occupancy synchronization
- Daily occupancy scheduler
- Monthly rent payment generation
- Rent payment receipts
- Configurable rent reminder notifications
- Shop occupancy report
- Public shop listing and interest web form

## 🛡️ Business Validations

- Shop area must be greater than zero
- Rent amount cannot be negative
- Contract end date cannot precede start date
- Occupied shops require a tenant
- Prevent conflicting tenant assignments
- Prevent overlapping submitted rental contracts
- Automatically update shop occupancy based on active contracts

## 🧪 Automated Testing

The application includes 11 automated integration tests.

- Airport Shop: 5 tests
- Shop Rental Contract: 6 tests

Run tests:

```bash
bench --site your-test-site.localhost run-tests \
  --module airplane_mode.airport_shop_management.doctype.airport_shop.test_airport_shop

bench --site your-test-site.localhost run-tests \
  --module airplane_mode.airport_shop_management.doctype.shop_rental_contract.test_shop_rental_contract
```

## ⚙️ Installation

Requirements:

- Frappe Framework v16
- Bench CLI
- MariaDB and Redis

Install the application in an existing Frappe Bench:

```bash
bench get-app <repository-url>

bench --site your-site.local install-app airplane_mode

bench --site your-site.local migrate
```

## 📂 Main Modules

- **Airplane Mode:** Airline and flight operations.
- **Airport Shop Management:** Shops, tenants, rental contracts, payments, and reporting.

## 🛠️ Technologies

Python · Frappe Framework · JavaScript · Jinja · MariaDB · REST API

## 👨‍💻 Developer

Mahmoud Khaled
