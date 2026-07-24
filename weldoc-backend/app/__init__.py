from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from app.database import db
from app.routes import register_routes
import os


def create_app():
    frontend_folder = os.path.join(os.path.dirname(__file__), '..', 'weldoc')
    app = Flask(__name__, static_folder=os.path.abspath(frontend_folder), static_url_path='')
    app.config.from_object("app.config.Config")

    CORS(app)
    db.init_app(app)

    register_routes(app)

    @app.route("/")
    def serve_index():
        return send_from_directory(app.static_folder, 'index.html')

    @app.route("/<path:path>")
    def serve_frontend(path):
        file_path = os.path.join(app.static_folder, path)
        if os.path.isfile(file_path):
            return send_from_directory(app.static_folder, path)
        return jsonify({"error": "not found"}), 404

    with app.app_context():
        db.create_all()

    return app
