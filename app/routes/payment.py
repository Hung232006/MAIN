from flask import Blueprint, jsonify, request, current_app, send_file, redirect, render_template
from flask_login import login_required, current_user
from datetime import datetime
import urllib.parse, hashlib, qrcode
from io import BytesIO
from app.models import CartItem, Order
from app import db
from .vnpay import vnpay
from .utils import get_client_ip

payment_bp = Blueprint("payment", __name__)

def get_cart_total():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    total_amount = sum(item.product.price * item.quantity for item in cart_items)
    return total_amount, cart_items

def create_vnpay_url(amount, cart_items):
    order_id = datetime.now().strftime("%Y%m%d%H%M%S")
    order_info = "Thanh toán giỏ hàng: " + ", ".join([f"{i.product.name} x{i.quantity}" for i in cart_items])

    vnp_params = {
        "vnp_Version": "2.1.0",
        "vnp_Command": "pay",
        "vnp_TmnCode": current_app.config.get("VNP_TMN_CODE"),  # an toàn
        "vnp_Amount": str(int(amount * 100)),
        "vnp_CurrCode": "VND",
        "vnp_TxnRef": order_id,
        "vnp_OrderInfo": order_info,
        "vnp_OrderType": "billpayment",
        "vnp_Locale": "vn",
        "vnp_ReturnUrl": current_app.config.get("VNP_RETURN_URL"),
        "vnp_IpAddr": request.remote_addr,
        "vnp_CreateDate": datetime.now().strftime("%Y%m%d%H%M%S"),
    }

    sorted_params = sorted(vnp_params.items())
    query_string = urllib.parse.urlencode(sorted_params)
    hash_data = "&".join([f"{k}={v}" for k, v in sorted_params])
    secure_hash = hashlib.sha512((current_app.config.get("VNP_HASH_SECRET", "") + hash_data).encode("utf-8")).hexdigest()
    return f"{current_app.config.get('VNP_URL')}?{query_string}&vnp_SecureHash={secure_hash}"

# --- QR code thanh toán ---
@payment_bp.route("/payment_qr/")
@login_required
def payment_qr():
    amount, cart_items = get_cart_total()
    if amount <= 0:
        return "Giỏ hàng trống!", 400
    payment_url = create_vnpay_url(amount, cart_items)
    img = qrcode.make(payment_url)
    buf = BytesIO()
    img.save(buf)
    buf.seek(0)
    return send_file(buf, mimetype='image/png')

# --- Thanh toán redirect ---
@payment_bp.route("/payment", methods=["GET", "POST"])
@login_required
def payment():
    if request.method == "POST":
        method = request.form.get("method")
        order_id = request.form.get("order_id")
        amount = int(request.form.get("amount", 0))
        order_desc = request.form.get("order_desc")
        order_type = request.form.get("order_type")
        bank_code = request.form.get("bank_code")
        language = request.form.get("language")
        ipaddr = get_client_ip(request)

        if method == "cash":
            order = Order(txn_ref=order_id, amount=amount, status="pending")
            db.session.add(order)
            db.session.commit()
            return "Đơn hàng đã được tạo, thanh toán khi nhận hàng."
        elif method == "vnpay":
            vnp = vnpay()
            vnp.requestData['vnp_Version'] = '2.1.0'
            vnp.requestData['vnp_Command'] = 'pay'
            vnp.requestData['vnp_TmnCode'] = current_app.config.get("VNP_TMN_CODE")
            vnp.requestData['vnp_Amount'] = amount * 100
            vnp.requestData['vnp_CurrCode'] = 'VND'
            vnp.requestData['vnp_TxnRef'] = order_id
            vnp.requestData['vnp_OrderInfo'] = order_desc
            vnp.requestData['vnp_OrderType'] = order_type
            vnp.requestData['vnp_Locale'] = language if language else 'vn'
            if bank_code:
                vnp.requestData['vnp_BankCode'] = bank_code
            vnp.requestData['vnp_CreateDate'] = datetime.now().strftime('%Y%m%d%H%M%S')
            vnp.requestData['vnp_IpAddr'] = ipaddr
            vnp.requestData['vnp_ReturnUrl'] = current_app.config.get("VNP_RETURN_URL")

            vnpay_payment_url = vnp.get_payment_url(
    current_app.config.get("VNP_URL"),
    current_app.config.get("VNP_HASH_SECRET")
)

            return redirect(vnpay_payment_url)
        else:
            return "Phương thức thanh toán không hợp lệ!"
    else:
        order_id = "DH" + datetime.now().strftime("%Y%m%d%H%M%S")
        return render_template("checkout.html", order_id=order_id, title="Thanh toán")
