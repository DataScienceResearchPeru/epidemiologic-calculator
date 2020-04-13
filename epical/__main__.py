from . import create_app
from .app import app
from .conf import Settings

EPICAL_APP = create_app(app)

if __name__ == "__main__":
    EPICAL_APP.run(
        host="127.0.0.1", port=Settings.PORT, debug=Settings.MODE_DEBUGGER,
    )
