"""
Script để thêm sản phẩm vào database MySQL
Chạy: python add_products.py
"""
from app import create_app, db
from app.models import Product

def add_sample_products():
    """Thêm các sản phẩm mẫu vào database"""
    app = create_app()
    with app.app_context():
        try:
            # Kiểm tra xem sản phẩm đã tồn tại chưa
            if Product.query.count() > 0:
                print("✓ Database đã có sản phẩm!")
                products = Product.query.all()
                for p in products:
                    print(f"  - {p.id}: {p.name} - {p.price:,.0f}đ")
                return
            
            # Thêm sản phẩm mẫu
            sample_products = [
                Product(name='Giày Sneaker Da', price=450000),
                Product(name='Giày Sneaker Cổ Trung Xám', price=600000),
                Product(name='Giày Chạy Adidas', price=750000),
                Product(name='Giày Sneaker', price=500000),
                Product(name='Giày Dày', price=350000),
                Product(name='Giày Cao Cổ Đỏ', price=550000),
                Product(name='Giày Sneaker Đế Dày', price=500000),
                Product(name='Giày Trắng Xanh Nhẹ', price=450000),
                Product(name='Giày Chạy Thể Thao', price=500000),
            ]
            
            db.session.add_all(sample_products)
            db.session.commit()
            
            print("✓ Đã thêm các sản phẩm vào database thành công!")
            
            # Hiển thị sản phẩm vừa thêm
            products = Product.query.all()
            print(f"\nTổng cộng: {len(products)} sản phẩm")
            for p in products:
                print(f"  - {p.id}: {p.name} - {p.price:,.0f}đ")
                
        except Exception as e:
            print(f"✗ Lỗi khi thêm sản phẩm: {e}")
            db.session.rollback()
            return False
    
    return True

if __name__ == '__main__':
    add_sample_products()
