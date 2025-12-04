from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user
from ..models import User
from .. import db   # dùng .. thay vì app để tránh vòng lặp import

# 🔹 Khai báo blueprint trước
auth_bp = Blueprint('auth', __name__)

# 🔹 Sau đó mới định nghĩa route
@auth_bp.route('/profile')
def profile():
    return "Trang tài khoản của bạn"

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    message = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.pass_field, password):
            login_user(user)
            return redirect(url_for('main.index'))
        else:
            message = "Sai email hoặc mật khẩu"

    return render_template('login.html', message=message)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    message = None
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        requestpass = request.form['requestpass']

        if password != requestpass:
            message = "Mật khẩu xác nhận không khớp"
            return render_template('login.html', message=message)

        if User.query.filter_by(email=email).first():
            message = "Email đã tồn tại"
            return render_template('login.html', message=message)

        hashed_pw = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(nameusers=username, email=email, pass_field=hashed_pw)
        db.session.add(new_user)
        db.session.commit()

        message = "Đăng ký thành công, hãy đăng nhập"
        return render_template('login.html', message=message)

    return render_template('login.html', message=message)


@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
