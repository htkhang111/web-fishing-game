import random
from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required, current_user
from app.models import FishConfig, Inventory, db

# Định nghĩa Blueprint
game_bp = Blueprint('game', __name__)

# --- TRANG CHỦ GAME ---
@game_bp.route('/')
@login_required
def index():
    # Lấy danh sách túi đồ của người chơi hiện tại
    inventory = Inventory.query.filter_by(user_id=current_user.id).all()
    return render_template('game.html', inventory=inventory)

# --- API: CÂU CÁ (Weighted Random) ---
@game_bp.route('/api/catch', methods=['POST'])
@login_required
def catch_fish():
    # 1. Lấy tất cả loại cá từ DB
    all_fishes = FishConfig.query.all()
    if not all_fishes:
        return jsonify({'status': 'error', 'message': 'Chưa có dữ liệu cá (Hãy chạy init_db.py)!'}), 500

    # 2. Thuật toán Random theo độ hiếm
    # Rarity càng cao (5) thì trọng số càng nhỏ (1/5) -> Khó trúng
    weights = [1 / f.rarity for f in all_fishes]
    
    # Chọn ngẫu nhiên 1 con
    caught_fish = random.choices(all_fishes, weights=weights, k=1)[0]

    # 3. Lưu vào túi đồ (Inventory)
    # Kiểm tra xem user đã có con này chưa
    inv_item = Inventory.query.filter_by(user_id=current_user.id, fish_id=caught_fish.id).first()
    
    if inv_item:
        inv_item.quantity += 1  # Có rồi thì tăng số lượng
    else:
        # Chưa có thì tạo mới
        new_item = Inventory(user_id=current_user.id, fish_id=caught_fish.id, quantity=1)
        db.session.add(new_item)

    # 4. Cộng kinh nghiệm
    current_user.exp += caught_fish.difficulty * 10
    
    db.session.commit()

    # Trả kết quả về cho Frontend hiển thị
    return jsonify({
        'status': 'success',
        'fish_name': caught_fish.name,
        'image': caught_fish.image_url,
        'rarity': caught_fish.rarity,
        'gold_value': caught_fish.base_price
    })

# --- API: BÁN CÁ ---
@game_bp.route('/api/sell', methods=['POST'])
@login_required
def sell_fish():
    data = request.json
    fish_id = data.get('fish_id')
    
    # Tìm cá trong túi
    item = Inventory.query.filter_by(user_id=current_user.id, fish_id=fish_id).first()
    
    if item and item.quantity > 0:
        # Tính tiền
        earn_gold = item.fish_details.base_price
        
        # Trừ số lượng, cộng tiền
        item.quantity -= 1
        if item.quantity == 0:
            db.session.delete(item) # Hết thì xóa dòng đó luôn
            
        current_user.gold += earn_gold
        db.session.commit()
        
        return jsonify({'status': 'success', 'new_gold': current_user.gold})
    
    return jsonify({'status': 'error', 'message': 'Không tìm thấy cá để bán!'}), 400