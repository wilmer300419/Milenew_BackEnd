from datetime import date, datetime, time

from flask import Flask, jsonify
from flask.json.provider import DefaultJSONProvider
from flask_cors import CORS
from config import config_dict
from src.database.database import Database

# Blueprints (capa de rutas)
from src.routes.auth.auth_routes import auth_bp
from src.routes.auth.user_routes import user_bp
from src.routes.auth.document_type_routes import document_type_bp
from src.routes.auth.registration_routes import registration_bp

# Excepciones de dominio
from src.utils.errors import NotFoundError, ConflictError


class ApiJSONProvider(DefaultJSONProvider):
    """Fechas/horas en formato ISO (ej. 2026-09-30) para que el front las lea facil."""

    def default(self, o):
        if isinstance(o, (date, datetime, time)):
            return o.isoformat()
        return super().default(o)


def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(document_type_bp)
    app.register_blueprint(registration_bp)


def register_error_handlers(app):
    """Traduce excepciones a respuestas JSON con su codigo HTTP."""

    @app.errorhandler(ValueError)
    def handle_validation(e):
        return jsonify({"error": "validation_error", "message": str(e)}), 400

    @app.errorhandler(NotFoundError)
    def handle_not_found(e):
        return jsonify({"error": "not_found", "message": str(e)}), 404

    @app.errorhandler(ConflictError)
    def handle_conflict(e):
        return jsonify({"error": "conflict", "message": str(e)}), 409

    @app.errorhandler(ConnectionError)
    def handle_db_down(e):
        return jsonify({"error": "database_unavailable", "message": str(e)}), 503

    @app.errorhandler(NotImplementedError)
    def handle_stand_by(e):
        return jsonify({"error": "not_implemented", "message": str(e)}), 501

    @app.errorhandler(404)
    def handle_route_not_found(e):
        return jsonify({"error": "not_found", "message": "Ruta no encontrada."}), 404

    @app.errorhandler(405)
    def handle_method_not_allowed(e):
        return jsonify({"error": "method_not_allowed", "message": "Metodo no permitido."}), 405

    @app.errorhandler(Exception)
    def handle_unexpected(e):
        # Ultima red de seguridad: no filtrar detalles internos
        return jsonify({"error": "internal_error", "message": "Error interno del servidor."}), 500


def create_app(config_name="default"):
    app = Flask(__name__)
    app.json = ApiJSONProvider(app)
    app.config.from_object(config_dict[config_name])

    # CORS: permite que el frontend (otro dominio/puerto) llame a la API.
    CORS(app)

    def check_db_connection():
        conn = Database.get_db_connection()
        if conn:
            print("Conexion inicial con PostgreSQL establecida.")
            conn.close()
        else:
            print("Aviso: no se pudo conectar a la base de datos (la API arranca igual).")

    check_db_connection()

    register_blueprints(app)
    register_error_handlers(app)

    @app.route("/", methods=["GET"])
    def health_check():
        conn = Database.get_db_connection()
        if conn:
            conn.close()
            return jsonify({
                "status": "online",
                "database": "connected",
                "message": "Milenew API funcionando correctamente."
            }), 200
        return jsonify({
            "status": "online",
            "database": "disconnected",
            "message": "La API esta arriba pero sin conexion a la base de datos."
        }), 200

    return app


app = create_app("development")

if __name__ == "__main__":
    port = app.config["PORT"]
    debug = app.config["DEBUG"]
    app.run(host="0.0.0.0", port=port, debug=debug)
