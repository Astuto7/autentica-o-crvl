import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-oficina-123')
    
    db_url = os.getenv('DATABASE_URL', 'sqlite:///auth.db')
    # Corrige a compatibilidade de URL do Postgres no Render
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
        
    SQLALCHEMY_DATABASE_URI = db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER_QR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static', 'qr')
