from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

# Initialize tools
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    # This pulls in your tables from models.py
    with app.app_context():
        import models 

    @app.route('/')
    def home():
        return jsonify({
            "status": "InternHub Online",
            "database": "Github_db Connected"
        })

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)