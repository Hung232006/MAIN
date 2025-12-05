from . import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import pytz



vn_tz = pytz.timezone("Asia/Ho_Chi_Minh")

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    nameusers = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    # Trường mật khẩu
    pass_field = db.Column("pass", db.String(255), nullable=False)

    # Check admin
    is_admin = db.Column(db.Boolean, default=False)

    requestpass = db.Column(db.String(255))

    # ----- Hàm xử lý mật khẩu -----
    def set_password(self, password):
        self.pass_field = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pass_field, password)


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    image = db.Column(db.String(255))
    description = db.Column(db.Text)
    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(vn_tz)  # giờ VN
    )


class CartItem(db.Model):
    __tablename__ = 'cart_items'
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)

    quantity = db.Column(db.Integer, default=1)
    size = db.Column(db.String(10))
    status = db.Column(db.String(20), nullable=False, default='pending')
    product = db.relationship('Product')
    user = db.relationship('User') 
    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(vn_tz)  # giờ VN
    )
