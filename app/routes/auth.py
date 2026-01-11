from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User, db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/', methods=['GET', 'POST'])
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('game.game'))
        else:
            flash('Sai tên đăng nhập hoặc mật khẩu!', 'danger')
            
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Kiểm tra user tồn tại
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Tên đăng nhập đã tồn tại!', 'warning')
            return redirect(url_for('auth.register'))
        
        # --- FIX LỖI Ở ĐÂY: Bỏ method='sha256' để dùng mặc định an toàn hơn ---
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Đăng ký thành công! Hãy đăng nhập.', 'success')
        return redirect(url_for('auth.login'))
        
    return render_template('login.html', register_mode=True)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))