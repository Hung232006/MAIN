from flask import Blueprint, request, current_app, send_file
from flask_login import current_user
from datetime import datetime
import urllib.parse, hashlib, qrcode
from io import BytesIO
from app.models import CartItem

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
        "vnp_TmnCode": current_app.config["VNP_TMN_CODE"],
        "vnp_Amount": str(int(amount * 100)),
        "vnp_CurrCode": "VND",
        "vnp_TxnRef": order_id,
        "vnp_OrderInfo": order_info,
        "vnp_OrderType": "billpayment",
        "vnp_Locale": "vn",
        "vnp_ReturnUrl": current_app.config["VNP_RETURN_URL"],
        "vnp_IpAddr": request.remote_addr,
        "vnp_CreateDate": datetime.now().strftime("%Y%m%d%H%M%S"),
    }

    sorted_params = sorted(vnp_params.items())
    query_string = urllib.parse.urlencode(sorted_params)
    hash_data = "&".join([f"{k}={v}" for k, v in sorted_params])
    secure_hash = hashlib.sha512((current_app.config["VNP_HASH_SECRET"] + hash_data).encode("utf-8")).hexdigest()
    return f"{current_app.config['VNP_URL']}?{query_string}&vnp_SecureHash={secure_hash}"

@payment_bp.route("/payment_qr/")
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

@payment_bp.route("/payment_return")
def payment_return():
    input_data = request.args.to_dict()
    vnp_secure_hash = input_data.pop("vnp_SecureHash", None)
    sorted_data = sorted(input_data.items())
    hash_data = "&".join([f"{k}={v}" for k, v in sorted_data])
    secure_hash = hashlib.sha512((current_app.config["VNP_HASH_SECRET"] + hash_data).encode("utf-8")).hexdigest()

    if secure_hash == vnp_secure_hash:
        if input_data.get("vnp_ResponseCode") == "00":
            # TODO: cập nhật trạng thái đơn hàng thành "đã thanh toán"
            return "Thanh toán thành công!"
        else:
            return f"Thanh toán không thành công! Mã lỗi: {input_data.get('vnp_ResponseCode')}"
    return "Sai chữ ký!"
