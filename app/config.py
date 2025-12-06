class Config:
    # Flask & Database
    SECRET_KEY = 'your-secret-key'
    SQLALCHEMY_DATABASE_URI = 'postgresql://quan_ly_kho_dev_user:qvt4p0PP4OMEdwn7jRgqgbiPdvk3HCma@dpg-d4q0qds9c44c73b44tpg-a.virginia-postgres.render.com/quan_ly_kho_dev'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # VNPay
    VNP_TMN_CODE = "YOUR_TMN_CODE"
    VNP_HASH_SECRET = "YOUR_SECRET_KEY"
    VNP_URL = "https://sandbox.vnpayment.vn/paymentv2/vpcpay.html"
    VNP_RETURN_URL = "https://duchungstore.onrender.com/payment_return"

