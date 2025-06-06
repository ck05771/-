from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'

    db.init_app(app)

    from .routes.main import main
    app.register_blueprint(main)

    with app.app_context():
        db.create_all()

    return app
