import os

# Lấy đường dẫn gốc của thư mục backend
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Key bảo mật cho session (thực tế nên để trong biến môi trường)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'key-bao-mat-cuc-manh-cua-truong-khuynh-han'
    
    # Đường dẫn file DB SQLite (nằm trong folder instance)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'instance', 'fishing.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False