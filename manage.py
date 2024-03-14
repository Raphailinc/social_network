from flask import Flask
from app.models import db
from app.routes import bp as app_bp
from flask_login import LoginManager
from app.models import User

from config import Config

def create_app(config_class=Config):
    app = Flask(__name__, template_folder='templates')
    app.config.from_object(config_class)
    app.config['UPLOAD_FOLDER'] = config_class.UPLOAD_FOLDER
    app.config['UPLOAD_POST_FOLDER'] = config_class.UPLOAD_POST_FOLDER

    db.init_app(app)

    app.register_blueprint(app_bp)

    login_manager = LoginManager()
    login_manager.login_view = 'app.login'
    login_manager.login_message_category = 'danger'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        with db.session() as session:
            return session.get(User, user_id)

    return app

if __name__ == '__main__':
    with create_app().app_context():
        db.create_all()
    create_app().run(debug=True)