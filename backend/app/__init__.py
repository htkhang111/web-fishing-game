import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

# Khởi tạo các extension
db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_class=Config):
    # --- CẤU HÌNH ĐƯỜNG DẪN FRONTEND ---
    # Lấy đường dẫn hiện tại của file __init__.py
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Trỏ ngược ra 2 cấp để lấy folder frontend (app -> backend -> root -> frontend)
    frontend_dir = os.path.join(current_dir, '..', '..', 'frontend')
    
    template_dir = os.path.join(frontend_dir, 'templates')
    static_dir = os.path.join(frontend_dir, 'static')

    # Khởi tạo Flask với đường dẫn template/static tùy chỉnh
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    app.config.from_object(config_class)

    # Init extensions với app
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login' # Tên hàm view khi chưa login

    # Đăng ký Blueprints (Routes)
    # Lưu ý: Import bên trong hàm để tránh lỗi vòng lặp (circular import)
    from app.routes.auth import auth_bp
    from app.routes.game import game_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(game_bp)
    
    # Route test nhanh để đảm bảo server chạy
    @app.route('/test')
    def test_connection():
        return "Server Backend đã kết nối thành công với Frontend!"

    return app