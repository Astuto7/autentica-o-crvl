import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'chave-secreta-oficina-777')
    
    db_url = os.environ.get('DATABASE_URL', 'sqlite:///oficina.db')
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
        
    SQLALCHEMY_DATABASE_URI = db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER_QR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static', 'qr')
