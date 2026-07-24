from app.routes.clients import clients_bp
from app.routes.projects import projects_bp
from app.routes.pipelines import pipelines_bp
from app.routes.materials import materials_bp
from app.routes.welds import welds_bp
from app.routes.persons import users_bp
from app.routes.builder_doc import builder_doc_bp
from app.routes.auth import auth_bp


def register_routes(app):
    app.register_blueprint(clients_bp, url_prefix="/api/clients")
    app.register_blueprint(projects_bp, url_prefix="/api/projects")
    app.register_blueprint(pipelines_bp, url_prefix="/api/pipelines")
    app.register_blueprint(materials_bp, url_prefix="/api/materials")
    app.register_blueprint(welds_bp, url_prefix="/api/welds")
    app.register_blueprint(users_bp, url_prefix="/api/users")
    app.register_blueprint(builder_doc_bp, url_prefix="/api/pipelines")
    app.register_blueprint(auth_bp)
