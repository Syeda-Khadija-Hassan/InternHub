from flask import Flask, jsonify
from config import Config
from extensions import db, migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # bind extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # IMPORTANT: import models AFTER db init
    with app.app_context():
        import models

    @app.route('/')
    def home():
        return jsonify({"status": "InternHub Online"})

    @app.route('/test-users')
    def test_users():
        from models import User
        users = User.query.all()
        return jsonify({
            "user_count": len(users),
            "users": [u.username for u in users]
        })

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)