# test_app.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'your_secret_key'

    db.init_app(app)

    @app.route('/')
    def index():
        return "Hello, Flask!"

    with app.app_context():
        db.create_all()  # Create tables if they don't exist

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
