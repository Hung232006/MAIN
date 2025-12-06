class Config:
    # Flask & Database
    SECRET_KEY = 'your-secret-key'
    SQLALCHEMY_DATABASE_URI = 'postgresql://quan_ly_kho_dev_user:qvt4p0PP4OMEdwn7jRgqgbiPdvk3HCma@dpg-d4q0qds9c44c73b44tpg-a.virginia-postgres.render.com/quan_ly_kho_dev'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

 # VNPay Config
VNP_TMN_CODE = "NJFA55LY"   # Mã định danh merchant
VNP_HASH_SECRET = "BN6AYXN4DSTT4ENVLFGUDHD96XV34UIM"  # Chuỗi bí mật tạo checksum
VNP_URL = "https://sandbox.vnpayment.vn/paymentv2/vpcpay.html"  # URL sandbox
VNP_RETURN_URL = "https://duchungstore.onrender.com/payment_return"  # URL nhận kết quả trả về
