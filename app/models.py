from . import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import pytz



vn_tz = pytz.timezone("Asia/Ho_Chi_Minh")

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)   # đổi từ nameusers -> username
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)                # đổi từ pass_field -> password
    is_admin = db.Column(db.Boolean, default=False)
    requestpass = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def set_password(self, raw_password):
        self.password = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        return check_password_hash(self.password, raw_password)



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
class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    txn_ref = db.Column(db.String(50), unique=True, nullable=False)   # vnp_TxnRef
    amount = db.Column(db.Integer, nullable=False)                    # số tiền
    status = db.Column(db.String(20), default="pending")              # pending/paid/failed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Quan hệ với User
    user = db.relationship("User", backref=db.backref("orders", lazy=True))