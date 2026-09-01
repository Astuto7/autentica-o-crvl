from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

class AuthRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    veiculo = db.Column(db.String(120), nullable=False)
    proprietario = db.Column(db.String(120), nullable=False)
    placa = db.Column(db.String(10), nullable=False)
    servico = db.Column(db.String(255), nullable=True, default="Revisão Geral e Autenticação Técnica")
    data_autenticacao = db.Column(db.DateTime, default=datetime.utcnow)
    token = db.Column(db.String(64), unique=True, nullable=False)
    qr_code_file = db.Column(db.String(120), nullable=True)
