import os
import uuid
import qrcode
from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from models import db, Admin, AuthRecord

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        admin = Admin.query.filter_by(username=username).first()

        if admin and check_password_hash(admin.password_hash, password):
            login_user(admin)
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Usuário ou senha inválidos.', 'danger')

    return render_template('admin/login.html')

@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('admin.login'))

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    registros = AuthRecord.query.order_by(AuthRecord.data_autenticacao.desc()).all()
    return render_template('admin/dashboard.html', registros=registros)

@admin_bp.route('/criar', methods=['GET', 'POST'])
@login_required
def create_auth():
    if request.method == 'POST':
        veiculo = request.form.get('veiculo')
        proprietario = request.form.get('proprietario')
        placa = request.form.get('placa', '').upper()
        servico = request.form.get('servico')

        token = str(uuid.uuid4())[:12]
        qr_filename = f"qr_{token}.png"
        qr_folder = current_app.config.get('UPLOAD_FOLDER_QR', 'static/qr')
        os.makedirs(qr_folder, exist_ok=True)
        qr_path = os.path.join(qr_folder, qr_filename)

        view_url = request.host_url.rstrip('/') + url_for('auth.view_record', token=token)
        qr_img = qrcode.make(view_url)
        qr_img.save(qr_path)

        novo_registro = AuthRecord(
            veiculo=veiculo,
            proprietario=proprietario,
            placa=placa,
            servico=servico,
            token=token,
            qr_code_file=qr_filename
        )
        db.session.add(novo_registro)
        db.session.commit()

        flash('Autenticação veicular gerada com sucesso!', 'success')
        return redirect(url_for('admin.dashboard'))

    return render_template('admin/create_auth.html')

