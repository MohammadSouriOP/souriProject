from flask import Flask

from src.presentation.errors_handlers.error_handlers import error_handlers
from src.presentation.routes import routes


def create_app():
    app = Flask(__name__)

    routes(app)
    error_handlers(app)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
