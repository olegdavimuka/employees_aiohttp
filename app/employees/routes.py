from views import EmployeeView, index


def setup_routes(app):
    app.router.add_get("/", index)
    app.router.add_view("/employees", EmployeeView)
