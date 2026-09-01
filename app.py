import os
from flask import Flask, redirect, url_for
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
from config import Config
from models import db, Admin
from admin import admin_bp
from auth import auth_bp

# Criação direta da instância para o Gunicorn
app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'admin.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    try:
        return Admin.query.get(int(user_id))
    except Exception:
        return None

app.register_blueprint(admin_bp)
app.register_blueprint(auth_bp)

@app.route('/')
def index():
    return redirect(url_for('admin.login'))

# Garante criação de diretório e tabelas
with app.app_context():
    try:
        qr_folder = os.path.join(app.root_path, 'static', 'qr')
        os.makedirs(qr_folder, exist_ok=True)
        db.create_all()
        if not Admin.query.filter_by(username='admin').first():
            novo_admin = Admin(
                username='admin',
                password_hash=generate_password_hash('admin123')
            )
            db.session.add(novo_admin)
            db.session.commit()
    except Exception as e:
        print(f"Aviso na inicialização do banco: {e}")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
