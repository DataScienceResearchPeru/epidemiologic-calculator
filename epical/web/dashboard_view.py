from flask import render_template
from flask.views import MethodView


class DashboardView(MethodView):
    @staticmethod
    def get():
        return render_template("dashboard.html")
