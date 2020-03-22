from flask import Flask

from web.dashboard_view import DashboardView


def configure_web_route(app: Flask):
    app.add_url_rule('/', view_func=DashboardView.as_view("dashboard"))
