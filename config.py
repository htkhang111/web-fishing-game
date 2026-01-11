import os

class Config:
    # Key bảo mật cho session
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev_key_very_secret_khong_bao_gio_doan_duoc'
    
    # Cấu hình Database SQLite
    SQLALCHEMY_DATABASE_URI = 'sqlite:///fishing_game.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # [QUAN TRỌNG] Link trỏ tới kho ảnh trên GitHub Pages của ông
    ASSETS_BASE_URL = 'https://htkhang111.github.io/angler-assets'