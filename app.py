from flask import Flask, jsonify
from config import Config
from extensions import db, migrate

# ----------------------------
# App Factory
# ----------------------------
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # bind extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # import models AFTER db init (IMPORTANT)
    with app.app_context():
        import models

    # ----------------------------
    # BASIC ROUTES
    # ----------------------------
    @app.route('/')
    def home():
        return jsonify({
            "status": "InternHub Online",
            "message": "Backend running successfully 🚀"
        })

    # ----------------------------
    # USER API
    # ----------------------------
    @app.route('/api/users', methods=['GET'])
    def get_users():
        from models import User

        users = User.query.all()

        return jsonify({
            "count": len(users),
            "users": [
                {
                    "user_id": u.user_id,
                    "username": u.username,
                    "email": u.email,
                    "is_active": u.is_active
                }
                for u in users
            ]
        })

    # ----------------------------
    # REPOSITORIES API
    # ----------------------------
    @app.route('/api/repositories', methods=['GET'])
    def get_repositories():
        from models import Repository

        repos = Repository.query.order_by(Repository.stars.desc()).limit(50).all()

        return jsonify({
            "count": len(repos),
            "repositories": [
                {
                    "repo_id": r.repo_id,
                    "full_name": r.full_name,
                    "owner": r.owner,
                    "language": r.language,
                    "stars": r.stars,
                    "forks": r.forks,
                    "url": r.html_url
                }
                for r in repos
            ]
        })

    # ----------------------------
    # ISSUES API
    # ----------------------------
    @app.route('/api/issues', methods=['GET'])
    def get_issues():
        from models import Issue

        issues = Issue.query.filter_by(state='open').limit(50).all()

        return jsonify({
            "count": len(issues),
            "issues": [
                {
                    "issue_id": i.issue_id,
                    "title": i.title,
                    "repo_id": i.repo_id,
                    "complexity": float(i.complexity_score) if i.complexity_score else None,
                    "estimated_time": float(i.estimated_time_hours) if i.estimated_time_hours else None
                }
                for i in issues
            ]
        })

    # ----------------------------
    # RECOMMENDATIONS API
    # ----------------------------
    @app.route('/api/recommendations', methods=['GET'])
    def get_recommendations():
        from models import Recommendation, Issue, Repository

        recs = Recommendation.query.order_by(Recommendation.score.desc()).limit(20).all()

        return jsonify({
            "count": len(recs),
            "recommendations": [
                {
                    "user_id": r.user_id,
                    "issue_id": r.issue_id,
                    "score": float(r.score),
                    "generated_at": r.generated_at
                }
                for r in recs
            ]
        })

    # ----------------------------
    # TEST ROUTE (DEBUG ONLY)
    # ----------------------------
    @app.route('/test-users')
    def test_users():
        from models import User

        users = User.query.all()

        return jsonify({
            "user_count": len(users),
            "users": [u.username for u in users]
        })

    return app


# ----------------------------
# RUN SERVER
# ----------------------------
if __name__ == '__main__':
    app = create_app()
    print("InternHub Backend Running on http://127.0.0.1:5000")
    app.run(debug=True)