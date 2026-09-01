import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'chave-oficina-segura-2026')
    
    # Tratamento automático de URI para SQLite local e PostgreSQL no Render
    raw_db_url = os.environ.get('DATABASE_URL', 'sqlite:///oficina.db')
    if raw_db_url.startswith("postgres://"):
        raw_db_url = raw_db_url.replace("postgres://", "postgresql://", 1)
        
    SQLALCHEMY_DATABASE_URI = raw_db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
