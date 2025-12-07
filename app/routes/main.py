from datetime import datetime
from flask import Blueprint, current_app, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user, login_user, logout_user
from app.models import db, User, Product, CartItem
from app.routes.payment import get_cart_total

main_bp = Blueprint("main", __name__)

# ============================
# TRANG CHỦ
# ============================
@main_bp.route("/")
@login_required
def index():
    products = Product.query.all()
    return render_template("_index.html", products=products)

# ============================
# TRANG ADMIN
# ============================
@main_bp.route("/admin")
@login_required
def admin_page():
    if not current_user.is_admin:
        flash("Bạn không có quyền truy cập trang admin!")
        return redirect(url_for("main.index"))
    return render_template("admin.html")

# ============================
# TẠO ADMIN
# ============================
@main_bp.route("/create_admin", methods=["GET", "POST"])
def create_admin():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        if User.query.filter_by(username=username).first():
            flash("Tên đăng nhập đã tồn tại!")
            return redirect(url_for("main.create_admin"))

        new_admin = User(username=username, email=email, is_admin=True)
        new_admin.set_password(password)
        db.session.add(new_admin)
        db.session.commit()

        flash("Tạo tài khoản admin thành công!")
        return redirect(url_for("main.login_page"))

    return render_template("create_admin.html")

# ============================
# LOGIN
# ============================
@main_bp.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for("main.admin_page") if user.is_admin else url_for("main.index"))

        flash("Sai tài khoản hoặc mật khẩu!")

    return render_template("login.html")

# ============================
# LOGOUT
# ============================
@main_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.login_page"))

# ============================
# GIỎ HÀNG
# ============================
@main_bp.route("/cart")
@login_required
def view_cart():
    cart_items = db.session.query(CartItem, Product)\
        .join(Product, CartItem.product_id == Product.id)\
        .filter(CartItem.user_id == current_user.id)\
        .all()
    return render_template("cart.html", cart_items=cart_items)

@main_bp.route("/api/add-to-cart", methods=["POST"])
@login_required
def add_to_cart():
    try:
        data = request.get_json()
        product_name = data.get("product_name")
        size = data.get("size")
        quantity = data.get("quantity", 1)

        product = Product.query.filter_by(name=product_name).first()
        if not product:
            return jsonify({"success": False, "message": "Sản phẩm không tồn tại"}), 404

        existing_item = CartItem.query.filter_by(
            user_id=current_user.id,
            product_id=product.id,
            size=size
        ).first()

        if existing_item:
            existing_item.quantity += quantity
        else:
            cart_item = CartItem(
                user_id=current_user.id,
                product_id=product.id,
                quantity=quantity,
                size=size
            )
            db.session.add(cart_item)

        db.session.commit()
        return jsonify({"success": True, "message": "Đã thêm vào giỏ hàng"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 500

@main_bp.route("/api/remove-from-cart/<int:item_id>", methods=["DELETE"])
@login_required
def remove_from_cart(item_id):
    try:
        cart_item = CartItem.query.get(item_id)
        if not cart_item or cart_item.user_id != current_user.id:
            return jsonify({"success": False, "message": "Không tìm thấy sản phẩm"}), 404

        db.session.delete(cart_item)
        db.session.commit()
        return jsonify({"success": True, "message": "Đã xóa khỏi giỏ hàng"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 500

@main_bp.route("/api/update-cart-item/<int:item_id>", methods=["PUT"])
@login_required
def update_cart_item(item_id):
    try:
        data = request.get_json()
        quantity = data.get("quantity", 1)

        if quantity < 1:
            return jsonify({"success": False, "message": "Số lượng không hợp lệ"}), 400

        cart_item = CartItem.query.get(item_id)
        if not cart_item or cart_item.user_id != current_user.id:
            return jsonify({"success": False, "message": "Không tìm thấy sản phẩm"}), 404

        cart_item.quantity = quantity
        db.session.commit()
        return jsonify({"success": True, "message": "Cập nhật thành công"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 500

@main_bp.route("/api/check-login")
def check_login():
    return jsonify({"logged_in": current_user.is_authenticated})

@main_bp.route("/checkout")
@login_required
def checkout():
    total_amount, cart_items = get_cart_total()
    order_id = "DH" + datetime.now().strftime("%Y%m%d%H%M%S")
    return render_template(
        "checkout.html",
        order_id=order_id,
        amount=total_amount,
        cart_items=cart_items,
        title="Thanh toán"
    )
@main_bp.route("/payment_return")
def payment_return():
    input_data = request.args.to_dict()
    # xử lý dữ liệu trả về từ VNPAY
    return render_template("payment_return.html",
                           title="Kết quả thanh toán",
                           result="Thanh toán thành công" if input_data.get("vnp_ResponseCode") == "00" else "Thanh toán thất bại",
                           order_id=input_data.get("vnp_TxnRef"),
                           amount=int(input_data.get("vnp_Amount", "0")) // 100,
                           order_desc=input_data.get("vnp_OrderInfo"),
                           vnp_TransactionNo=input_data.get("vnp_TransactionNo"),
                           vnp_ResponseCode=input_data.get("vnp_ResponseCode"))
