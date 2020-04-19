from .app import EPICAL_APP
from .conf import Settings

if __name__ == "__main__":
    EPICAL_APP.run(
        host="127.0.0.1", port=Settings.PORT, debug=Settings.MODE_DEBUGGER,
    )
