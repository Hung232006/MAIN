from flask import Blueprint, request, current_app, send_file
from datetime import datetime
import urllib.parse, hashlib, qrcode
from io import BytesIO

payment_bp = Blueprint("payment", __name__)

def create_vnpay_url(amount):
    vnp_params = {
        "vnp_Version": "2.1.0",
        "vnp_Command": "pay",
        "vnp_TmnCode": current_app.config["VNP_TMN_CODE"],
        "vnp_Amount": amount * 100,
        "vnp_CurrCode": "VND",
        "vnp_TxnRef": datetime.now().strftime("%Y%m%d%H%M%S"),
        "vnp_OrderInfo": "Thanh toán đơn hàng",
        "vnp_OrderType": "billpayment",
        "vnp_Locale": "vn",
        "vnp_ReturnUrl": current_app.config["VNP_RETURN_URL"],
        "vnp_IpAddr": request.remote_addr,
        "vnp_CreateDate": datetime.now().strftime("%Y%m%d%H%M%S"),
    }

    sorted_params = sorted(vnp_params.items())
    query_string = urllib.parse.urlencode(sorted_params)
    hash_data = "&".join([f"{k}={v}" for k, v in sorted_params])
    secure_hash = hashlib.sha512(
        (current_app.config["VNP_HASH_SECRET"] + hash_data).encode("utf-8")
    ).hexdigest()
    return f"{current_app.config['VNP_URL']}?{query_string}&vnp_SecureHash={secure_hash}"

# Route QR code, amount optional
@payment_bp.route("/payment_qr/", defaults={"amount": 10000})
@payment_bp.route("/payment_qr/<int:amount>")
def payment_qr(amount):
    payment_url = create_vnpay_url(amount)
    img = qrcode.make(payment_url)
    buf = BytesIO()
    img.save(buf)
    buf.seek(0)
    return send_file(buf, mimetype='image/png')

# Route nhận kết quả thanh toán từ VNPay
@payment_bp.route("/payment_return")
def payment_return():
    input_data = request.args.to_dict()
    vnp_secure_hash = input_data.pop("vnp_SecureHash", None)
    sorted_data = sorted(input_data.items())
    hash_data = "&".join([f"{k}={v}" for k, v in sorted_data])
    secure_hash = hashlib.sha512(
        (current_app.config["VNP_HASH_SECRET"] + hash_data).encode("utf-8")
    ).hexdigest()

    if secure_hash == vnp_secure_hash:
        if input_data.get("vnp_ResponseCode") == "00":
            return "Thanh toán thành công!"
        else:
            return f"Thanh toán không thành công! Mã lỗi: {input_data.get('vnp_ResponseCode')}"
    return "Sai chữ ký!"
