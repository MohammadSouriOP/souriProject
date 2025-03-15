from flask import Flask

# from src.presentaion.error_handler import register_error_handlers
from src.presentation.routes import routes

app = Flask(__name__)

routes(app)
# register_error_handlers(app)

app.run(debug=True)
