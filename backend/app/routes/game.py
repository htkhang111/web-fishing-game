import random
from flask import Blueprint, render_template, jsonify, request, session
from flask_login import login_required, current_user
from app.models import FishConfig, Inventory, db

game_bp = Blueprint('game', __name__)

# Cấu hình độ khó (Sao -> Số nút cần nhảy)
DIFFICULTY_CONFIG = {
    1: {'knots': 5},  # 1 sao: 5 nút
    2: {'knots': 6},  # 2 sao: 6 nút
    3: {'knots': 7},  # 3 sao: 7 nút
    4: {'knots': 8},  # 4 sao: 8 nút
    5: {'knots': 10}  # 5 sao: 10 nút (Nhảy mỏi tay)
}

@game_bp.route('/')
@login_required
def index():
    inventory = Inventory.query.filter_by(user_id=current_user.id).all()
    return render_template('game.html', inventory=inventory)

# --- API 1: QUĂNG CẦN (Sinh Minigame) ---
@game_bp.route('/api/cast', methods=['POST'])
@login_required
def cast_line():
    # 1. Chọn cá ngẫu nhiên (nhưng chưa cho user biết là con gì)
    all_fishes = FishConfig.query.all()
    if not all_fishes:
        return jsonify({'status': 'error', 'message': 'Chưa có dữ liệu cá!'}), 500

    # Random cá theo trọng số (cá hiếm khó ra)
    weights = [1 / f.rarity for f in all_fishes]
    target_fish = random.choices(all_fishes, weights=weights, k=1)[0]
    
    # 2. Sinh Sequence (Chuỗi mũi tên) dựa trên độ hiếm (Sao)
    config = DIFFICULTY_CONFIG.get(target_fish.rarity, {'knots': 5})
    num_knots = config['knots']
    
    directions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
    colors_normal = ['green', 'blue'] # Màu an toàn
    
    challenge_sequence = []
    expected_inputs = [] # Lưu lại để lát nữa check
    
    for _ in range(num_knots):
        direction = random.choice(directions)
        
        # 30% tỉ lệ ra Trap (Màu đỏ)
        is_trap = random.random() < 0.3 
        
        if is_trap:
            color = 'red'
            # Trap: Input phải ngược lại
            if direction == 'UP': expected = 'DOWN'
            elif direction == 'DOWN': expected = 'UP'
            elif direction == 'LEFT': expected = 'RIGHT'
            elif direction == 'RIGHT': expected = 'LEFT'
        else:
            color = random.choice(colors_normal)
            expected = direction # Bình thường
            
        challenge_sequence.append({
            'dir': direction, # Hướng hiển thị
            'color': color    # Màu sắc
        })
        expected_inputs.append(expected)

    # 3. Lưu session để lát check (Chống hack nhẹ)
    session['pending_fish_id'] = target_fish.id
    session['expected_inputs'] = expected_inputs
    
    return jsonify({
        'status': 'success',
        'sequence': challenge_sequence,
        'rarity': target_fish.rarity # Để frontend biết chỉnh tốc độ thanh trượt nếu muốn
    })

# --- API 2: GIẬT CÁ (Xác nhận kết quả) ---
@game_bp.route('/api/catch', methods=['POST'])
@login_required
def catch_fish():
    data = request.json
    # Frontend gửi lên chuỗi nút người dùng đã bấm
    user_inputs = data.get('inputs', [])
    success_step2 = data.get('timing_success', False) # Kết quả thanh trượt Space
    
    # Kiểm tra Session
    pending_fish_id = session.get('pending_fish_id')
    expected_inputs = session.get('expected_inputs')
    
    if not pending_fish_id or not expected_inputs:
        return jsonify({'status': 'error', 'message': 'Bạn chưa quăng cần!'}), 400

    # 1. Check Bước 1: Nhảy nút (So sánh input user với expected)
    if user_inputs != expected_inputs:
        session.pop('pending_fish_id', None) # Xóa session để phạt
        return jsonify({'status': 'fail', 'message': 'Đứt cước! Nhảy sai nhịp rồi!'})

    # 2. Check Bước 2: Thanh trượt (Space)
    if not success_step2:
        session.pop('pending_fish_id', None)
        return jsonify({'status': 'fail', 'message': 'Hụt! Bấm Space trượt rồi!'})

    # --- NẾU THẮNG CẢ 2 ---
    fish = FishConfig.query.get(pending_fish_id)
    
    # Cộng đồ
    inv_item = Inventory.query.filter_by(user_id=current_user.id, fish_id=fish.id).first()
    if inv_item:
        inv_item.quantity += 1
    else:
        new_item = Inventory(user_id=current_user.id, fish_id=fish.id, quantity=1)
        db.session.add(new_item)
    
    current_user.exp += fish.difficulty * 10
    db.session.commit()
    
    # Dọn dẹp session
    session.pop('pending_fish_id', None)
    session.pop('expected_inputs', None)

    return jsonify({
        'status': 'success',
        'fish_name': fish.name,
        'image': fish.image_url,
        'rarity': fish.rarity,
        'gold_value': fish.base_price
    })

@game_bp.route('/api/sell', methods=['POST'])
@login_required
def sell_fish():
    # ... (Giữ nguyên code cũ) ...
    data = request.json
    fish_id = data.get('fish_id')
    item = Inventory.query.filter_by(user_id=current_user.id, fish_id=fish_id).first()
    if item and item.quantity > 0:
        earn_gold = item.fish_details.base_price
        item.quantity -= 1
        if item.quantity == 0:
            db.session.delete(item)
        current_user.gold += earn_gold
        db.session.commit()
        return jsonify({'status': 'success', 'new_gold': current_user.gold})
    return jsonify({'status': 'error', 'message': 'Không tìm thấy cá!'}), 400