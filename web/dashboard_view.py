from flask.views import MethodView
from flask import render_template


class DashboardView(MethodView):

    def __init__(self):
        pass

    def get(self):
        return render_template("dashboard.html")
