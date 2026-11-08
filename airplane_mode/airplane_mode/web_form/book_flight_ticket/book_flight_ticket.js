frappe.ready(function () {
    if (window.location.pathname.endsWith("/new")) {
        setTimeout(function () {
            frappe.web_form.set_value("flight_price", 2000);
            console.log("Flight Price Set Successfully!");
        }, 700);
    }
});