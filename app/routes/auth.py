from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user
from app.models import User, db

auth_bp = Blueprint('auth', __name__, url_prefix="/auth")


# ===== LOGIN =====
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)

            if user.is_admin:
                return redirect(url_for('admin.admin_dashboard'))
            return redirect(url_for('main.index'))

        flash("Sai tài khoản hoặc mật khẩu!")

    return render_template("login.html")   # <-- file chứa cả login + register


# ===== REGISTER =====
@auth_bp.route('/register', methods=['POST'])
def register():
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    requestpass = request.form.get("requestpass")

    if password != requestpass:
        return render_template("login.html", message="Mật khẩu không trùng khớp!")

    # kiểm tra trùng email
    if User.query.filter_by(email=email).first():
        return render_template("login.html", message="Email đã tồn tại!")

    # tạo user mới
    new_user = User(nameusers=username, email=email, is_admin=False)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    return render_template("login.html", message="Đăng ký thành công! Hãy đăng nhập.")


@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
