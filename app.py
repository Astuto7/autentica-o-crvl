import os
from flask import Flask, redirect, url_for
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
from config import Config
from models import db, Admin
from admin import admin_bp
from auth import auth_bp

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'admin.login'
login_manager.login_message = 'Faça login para acessar o painel.'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(Admin, int(user_id))

app.register_blueprint(admin_bp)
app.register_blueprint(auth_bp)

@app.route('/')
def index():
    return redirect(url_for('admin.login'))

# Garante a criação do banco e do admin ao inicializar
with app.app_context():
    qr_dir = app.config.get('UPLOAD_FOLDER_QR', os.path.join(app.root_path, 'static', 'qr'))
    os.makedirs(qr_dir, exist_ok=True)
    db.create_all()
    if not Admin.query.filter_by(username='admin').first():
        novo_admin = Admin(
            username='admin',
            password_hash=generate_password_hash('admin123')
        )
        db.session.add(novo_admin)
        db.session.commit()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
