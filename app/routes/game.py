from flask import Blueprint, render_template, jsonify, request, current_app
from flask_login import login_required, current_user
from app.models import GameState, db

game_bp = Blueprint('game', __name__)

@game_bp.route('/game')
@login_required
def game():
    # Lấy URL assets từ config để truyền xuống giao diện
    assets_url = current_app.config['ASSETS_BASE_URL']
    return render_template('game.html', name=current_user.username, assets_url=assets_url)

@game_bp.route('/save_score', methods=['POST'])
@login_required
def save_score():
    data = request.get_json()
    score = data.get('score', 0)
    
    new_state = GameState(user_id=current_user.id, score=score)
    db.session.add(new_state)
    db.session.commit()
    
    return jsonify({'success': True, 'new_score': score})