from flask.views import MethodView


class DashboardView(MethodView):

    def __init__(self):
        pass

    def get(self):
        return 'Hello world'
