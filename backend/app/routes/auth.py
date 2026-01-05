from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User
from app import db

# Tạo Blueprint cho auth
auth_bp = Blueprint('auth', __name__)

# --- 1. ĐĂNG NHẬP ---
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Nếu đã đăng nhập rồi thì đá sang trang game luôn
    if current_user.is_authenticated:
        return redirect(url_for('game.index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Tìm user trong DB
        user = User.query.filter_by(username=username).first()
        
        # Kiểm tra password
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('game.index'))
        else:
            flash('Sai tên đăng nhập hoặc mật khẩu!', 'error')

    return render_template('login.html')

# --- 2. ĐĂNG KÝ ---
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('game.index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Kiểm tra trùng tên
        if User.query.filter_by(username=username).first():
            flash('Tên đăng nhập đã tồn tại! Vui lòng chọn tên khác.', 'error')
            return redirect(url_for('auth.register'))
        
        # Tạo user mới
        new_user = User(username=username)
        new_user.set_password(password)
        
        # Tặng quà tân thủ (100 vàng + cần câu level 1)
        new_user.gold = 100
        new_user.level = 1
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Đăng ký thành công! Hãy đăng nhập ngay.', 'success')
        return redirect(url_for('auth.login'))

    # Tạm thời dùng chung giao diện login, nhưng có thể tách ra nếu muốn
    return render_template('login.html', is_register=True)

# --- 3. ĐĂNG XUẤT ---
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Bạn đã đăng xuất thành công.', 'info')
    return redirect(url_for('auth.login'))