class Config:
    # Flask & Database
    SECRET_KEY = 'your-secret-key'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:CSDL2021@127.0.0.1/login'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # VNPay
    VNP_TMN_CODE = "YOUR_TMN_CODE"
    VNP_HASH_SECRET = "YOUR_SECRET_KEY"
    VNP_URL = "https://sandbox.vnpayment.vn/paymentv2/vpcpay.html"
    VNP_RETURN_URL = "http://localhost:5000/payment_return"
