import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

# Khởi tạo các extension
db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_class=Config):
    # --- CẤU HÌNH ĐƯỜNG DẪN FRONTEND (FIX ROBUST) ---
    # Lấy đường dẫn tuyệt đối của file này
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Đi ngược ra 2 cấp: app -> backend -> [ROOT] -> frontend
    # backend/app -> backend -> ROOT
    root_dir = os.path.dirname(os.path.dirname(current_dir)) 
    frontend_dir = os.path.join(root_dir, 'frontend')
    
    template_dir = os.path.join(frontend_dir, 'templates')
    static_dir = os.path.join(frontend_dir, 'static')

    # Khởi tạo Flask với đường dẫn template/static chính xác
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    app.config.from_object(config_class)

    # Init extensions với app
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login' # Tên hàm view khi chưa login

    # Đăng ký Blueprints (Routes)
    from app.routes.auth import auth_bp
    from app.routes.game import game_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(game_bp)
    
    @app.route('/test')
    def test_connection():
        return "Server Backend đã kết nối thành công với Frontend!"

    return app