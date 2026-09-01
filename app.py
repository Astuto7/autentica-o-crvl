import os
from flask import Flask, redirect, url_for
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
from config import Config
from models import db, Admin
from admin import admin_bp
from auth import auth_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'admin.login'
    login_manager.login_message = 'Faça login para acessar o painel.'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return Admin.query.get(int(user_id))

    app.register_blueprint(admin_bp)
    app.register_blueprint(auth_bp)

    @app.route('/')
    def index():
        return redirect(url_for('admin.login'))

    with app.app_context():
        os.makedirs(app.config.get('UPLOAD_FOLDER_QR', 'static/qr'), exist_ok=True)
        db.create_all()
        # Cria usuário admin padrão caso não exista
        if not Admin.query.filter_by(username='admin').first():
            novo_admin = Admin(
                username='admin',
                password_hash=generate_password_hash('admin123')
            )
            db.session.add(novo_admin)
            db.session.commit()

    return app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

