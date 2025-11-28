from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import login_required, current_user
from app.models import db, CartItem, Product

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@login_required
def index():
    products = Product.query.all()
    return render_template('_index.html', products=products)

@main_bp.route('/cart')
@login_required
def view_cart():
    user_id = current_user.id

    cart_items = db.session.query(CartItem, Product)\
        .join(Product, CartItem.product_id == Product.id)\
        .filter(CartItem.user_id == user_id)\
        .all()

    return render_template('cart.html', cart_items=cart_items)

@main_bp.route('/api/remove-from-cart/<int:item_id>', methods=['DELETE'])
@login_required
def remove_from_cart(item_id):
    """Xóa sản phẩm khỏi giỏ hàng"""
    try:
        cart_item = CartItem.query.get(item_id)
        
        # Kiểm tra xem item có tồn tại và thuộc về user không
        if not cart_item or cart_item.user_id != current_user.id:
            return jsonify({'success': False, 'message': 'Không tìm thấy sản phẩm'}), 404
        
        db.session.delete(cart_item)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Đã xóa khỏi giỏ hàng'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@main_bp.route('/api/update-cart-item/<int:item_id>', methods=['PUT'])
@login_required
def update_cart_item(item_id):
    """Cập nhật số lượng sản phẩm trong giỏ hàng"""
    try:
        data = request.get_json()
        quantity = data.get('quantity', 1)
        
        # Kiểm tra số lượng hợp lệ
        if quantity < 1:
            return jsonify({'success': False, 'message': 'Số lượng không hợp lệ'}), 400
        
        cart_item = CartItem.query.get(item_id)
        
        # Kiểm tra xem item có tồn tại và thuộc về user không
        if not cart_item or cart_item.user_id != current_user.id:
            return jsonify({'success': False, 'message': 'Không tìm thấy sản phẩm'}), 404
        
        cart_item.quantity = quantity
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Cập nhật thành công'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@main_bp.route('/checkout')
@login_required
def checkout():
    """Trang thanh toán"""
    return render_template('checkout.html')

@main_bp.route('/api/add-to-cart', methods=['POST'])
@login_required
def add_to_cart():
    """Thêm sản phẩm vào giỏ hàng"""
    try:
        data = request.get_json()
        product_name = data.get('product_name')
        size = data.get('size')
        quantity = data.get('quantity', 1)
        
        # Tìm sản phẩm theo tên
        product = Product.query.filter_by(name=product_name).first()
        if not product:
            return jsonify({'success': False, 'message': 'Sản phẩm không tồn tại'}), 404
        
        # Kiểm tra xem sản phẩm đã có trong giỏ không
        existing_item = CartItem.query.filter_by(
            user_id=current_user.id,
            product_id=product.id,
            size=size
        ).first()
        
        if existing_item:
            # Nếu có rồi thì tăng số lượng
            existing_item.quantity += quantity
        else:
            # Nếu chưa có thì tạo mới
            cart_item = CartItem(
                user_id=current_user.id,
                product_id=product.id,
                quantity=quantity,
                size=size
            )
            db.session.add(cart_item)
        
        db.session.commit()
        return jsonify({'success': True, 'message': 'Đã thêm vào giỏ hàng'}), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500
        