from flask import Flask

from .dashboard_view import DashboardView


def setup_web_routes(app: Flask):
    app.add_url_rule("/", view_func=DashboardView.as_view("dashboard"))
