from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from sqlalchemy import func
from ..models import CartItem, Product
from .. import db

admin_bp = Blueprint('admin', __name__, url_prefix="/admin")


@admin_bp.route('/dashboard')
@login_required
def admin_dashboard():
    # Tổng doanh thu
    total_sales = (
        db.session.query(func.sum(CartItem.quantity * Product.price))
        .join(Product, CartItem.product_id == Product.id)   # join qua product_id
        .scalar()
    ) or 0

    # Tổng sản lượng đã bán
    total_quantity = (
    db.session.query(func.coalesce(func.sum(CartItem.quantity), 0))
    .filter(CartItem.status == 'paid')
    .scalar()
)


    # Lấy tất cả cart items
    carts = (
        CartItem.query.join(Product)
        .order_by(CartItem.created_at.desc())
        .all()
    )

    return render_template(
        'admin.html',
        total_sales=total_sales,
        total_quantity=total_quantity,
        carts=carts
    )


# Cập nhật trạng thái đơn hàng
@admin_bp.route('/update_order/<int:cart_id>', methods=['POST'])
@login_required
def update_order(cart_id):
    # Kiểm tra quyền admin trước
    if not current_user.is_admin:
        return "Bạn không có quyền truy cập", 403

    cart = CartItem.query.get_or_404(cart_id)
    new_status = request.form.get('status')

    if new_status not in ['pending', 'paid', 'cancelled']:
        flash("Trạng thái không hợp lệ!", "danger")
        return redirect(url_for('admin.admin_dashboard'))

    cart.status = new_status
    db.session.commit()
    flash(f"Cập nhật đơn hàng {cart.id} thành công!", "success")
    return redirect(url_for('admin.admin_dashboard'))
