from flask import Flask
from .models import db
from .routes import workout_bp
from .form_routes import form_bp
import os

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object('app.config.Config')

    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(workout_bp, url_prefix='/api/workouts')
    app.register_blueprint(form_bp)
    return app
