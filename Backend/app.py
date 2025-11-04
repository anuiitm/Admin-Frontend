from flask import Flask, send_from_directory, current_app
from flask_cors import CORS
import os

from models import db


def create_app():
    app = Flask(__name__)

    # Basic config
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL", f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database.db')}"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JSON_SORT_KEYS"] = False
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret")
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'static', 'uploads')

    # Ensure the folder actually exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # CORS for local dev frontend (Vite default port)
    CORS(app, resources={r"/api/*": {"origins": ["http://localhost:5173", "http://127.0.0.1:5173"]}})

    # Initialize DB
    db.init_app(app)

    # Register blueprints
    from routes import api_bp
    app.register_blueprint(api_bp, url_prefix="/api/admin")

    @app.route("/health")
    def health():
        return {"status": "ok"}

    return app


if __name__ == "__main__":
    application = create_app()
    with application.app_context():
        db.create_all()
    application.run(host="0.0.0.0", port=int(os.getenv("PORT", 5001)), debug=True)


