from . import app
from .conf import Settings

if __name__ == "__main__":
    app.run(
        host=Settings.HOST, port=Settings.PORT, debug=Settings.MODE_DEBUGGER,
    )
