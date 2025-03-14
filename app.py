from flask import Flask
from src.presentaion.routes import register_routes
from src.presentaion.error_handler import register_error_handlers

app = Flask(__name__)

register_routes(app)
register_error_handlers(app)

app.run(debug=True)
