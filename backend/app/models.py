from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# --- 1. BẢNG NGƯỜI CHƠI (USER) ---
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    
    # Chỉ số game
    gold = db.Column(db.Integer, default=0)       # Tiền vàng
    level = db.Column(db.Integer, default=1)      # Cấp độ cần câu
    exp = db.Column(db.Integer, default=0)        # Kinh nghiệm
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Quan hệ: Một người có nhiều món trong túi đồ
    inventory_items = db.relationship('Inventory', backref='owner', lazy='dynamic')

    # Hàm xử lý mật khẩu
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username} - Lvl {self.level}>'

# Hàm hỗ trợ Flask-Login tìm user qua ID
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


# --- 2. BẢNG CẤU HÌNH CÁ (FISH CONFIG) ---
class FishConfig(db.Model):
    __tablename__ = 'fish_config'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    image_url = db.Column(db.String(256))  # Đường dẫn ảnh cá
    
    # Thông số game
    rarity = db.Column(db.Integer, default=1)      # Độ hiếm (1-5 sao)
    base_price = db.Column(db.Integer, default=10) # Giá bán cơ bản
    difficulty = db.Column(db.Integer, default=1)  # Độ khó minigame (tốc độ thanh trượt)
    
    def __repr__(self):
        return f'<Fish {self.name} - {self.base_price}G>'


# --- 3. BẢNG TÚI ĐỒ (INVENTORY) ---
class Inventory(db.Model):
    __tablename__ = 'inventory'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    fish_id = db.Column(db.Integer, db.ForeignKey('fish_config.id'))
    
    quantity = db.Column(db.Integer, default=1)
    caught_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Quan hệ để lấy thông tin chi tiết của con cá từ Inventory
    fish_details = db.relationship('FishConfig')

    def __repr__(self):
        return f'<Inv: User {self.user_id} has Fish {self.fish_id} x{self.quantity}>'