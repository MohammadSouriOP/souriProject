from flask import Flask

from src.presentation.errors_handlers.error_handlers import error_handlers
from src.presentation.routes import routes

app = Flask(__name__)

routes(app)
error_handlers(app)

app.run(debug=True)
