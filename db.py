from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db_app(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["JWT_SECRET_KEY"] = "super-secret-123"  # Change this!

    db.init_app(app)
    with app.app_context():
        db.create_all()