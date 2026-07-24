from flask import Flask
from flask_cors import CORS
from app.database import db
from app.routes import register_routes


def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    CORS(app)
    db.init_app(app)

    register_routes(app)

    with app.app_context():
        db.create_all()

    return app
