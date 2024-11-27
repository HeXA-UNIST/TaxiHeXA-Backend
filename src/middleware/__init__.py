from flask import Flask

from .middleware import db, cors, migrate, session, socketio, ma, mail, admin
from config import Config


def create_app(config: Config):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    cors.init_app(app)
    migrate.init_app(app, db)
    session.init_app(app)
    socketio.init_app(app)
    ma.init_app(app)
    mail.init_app(app)
    admin.init_app(app)

    with app.app_context():
        db.create_all()

    return app, socketio