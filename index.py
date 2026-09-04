from flask import Flask, jsonify
from config import config_dict
from src.database.database import Database  # <- Cambio aquí (se agrega src.)

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config_dict[config_name])

    def check_db_connection():
        conn = Database.get_db_connection()
        if conn:
            print("Successfully connected to the PostgreSQL database.")
            conn.close()
        else:
            print("Failed to establish initial connection with the database.")

    check_db_connection()

    @app.route('/', methods=['GET'])
    def health_check():
        conn = Database.get_db_connection()
        if conn:
            conn.close()
            return jsonify({
                "status": "online",
                "database": "connected",
                "message": "Transport API is running smoothly."
            }), 200
            
        return jsonify({
            "status": "online",
            "database": "disconnected",
            "message": "Database connection error."
        }), 500

    return app


app = create_app('development')

if __name__ == '__main__':
    port = app.config['PORT']
    debug = app.config['DEBUG']
    app.run(host='0.0.0.0', port=port, debug=debug)