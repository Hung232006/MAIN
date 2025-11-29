create database if not exists login;
USE login;

-- Bảng người dùng
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    requestpass VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Bảng sản phẩm
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    image VARCHAR(255),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Bảng giỏ hàng
CREATE TABLE IF NOT EXISTS cart_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT DEFAULT 1,
    size VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);
DELETE p1 FROM products p1
JOIN products p2 ON p1.name = p2.name AND p1.id > p2.id;


INSERT INTO products (name, price, image, description)
VALUES
('Giày Sneaker Da', 450000, 'https://tamanh.net/wp-content/uploads/2022/01/shop-giay-da-lon.jpg', 'Sneaker da cao cấp'),
('Giày Cao Cổ', 550000, 'https://lh3.googleusercontent.com/6euB1qM538WNYNFPEl1w1sNM00sTlgr0KBRqk_CeOlMFGOqq2yEBqe49HIldpfv8oVypbiwsdoQ6VMUsamiyGr_JibvyKUon85vMJtAxihuOC80xF_6le7hsx3ptiYce1N5pEGDCRNDL9I2X4kZ5AXY', 'Giày cao cổ thời trang'),
('Giày Sneaker Cổ Trung Xám', 600000, 'https://file.hstatic.net/1000192210/file/cach-chup-giay-dep-3_4063194a64c74b86aa9433a3723f10dd.jpg', 'Sneaker cổ trung màu xám'),
('Giày Chạy Adidas', 750000, 'https://myshoes.vn/image/catalog/blog/26.11/mau-giay-the-thao-nam.jpeg', 'Giày chạy bộ Adidas chính hãng'),
('Giày Sneaker', 500000, 'https://cf.shopee.vn/file/ab0f21cda8ea0eb8b444a8f03365d088', 'Sneaker trẻ trung, năng động'),
('Giày Dày', 350000, 'https://lh3.googleusercontent.com/6euB1qM538WNYNFPEl1w1sNM00sTlgr0KBRqk_CeOlMFGOqq2yEBqe49HIldpfv8oVypbiwsdoQ6VMUsamiyGr_JibvyKUon85vMJtAxihuOC80xF_6le7hsx3ptiYce1N5pEGDCRNDL9I2X4kZ5AXY', 'Giày dày, chắc chắn'),
('Giày Cao Cổ Đỏ', 550000, 'https://salt.tikicdn.com/cache/w1200/ts/product/32/2e/aa/716e8f83bcfef3e249922c0685fd1247.jpg', 'Giày cao cổ màu đỏ nổi bật'),
('Giày Sneaker Đế Dày', 500000, 'https://vn-test-11.slatic.net/p/23248c8fb9647b30f8013baff44c8029.jpg', 'Sneaker đế dày cá tính'),
('Giày Trắng Xanh Nhẹ', 450000, 'https://media3.scdn.vn/img4/2023/04_08/XPkkUaOkcKS3tbLOwYGq.png', 'Giày trắng xanh nhẹ nhàng'),
('Giày Chạy Thể Thao', 500000, 'https://cf.shopee.vn/file/8c4bdfcb1341fe0db77ad6e1677a0c3b', 'Giày chạy thể thao bền bỉ');
#nếu muốn xóa sản phẩm và thêm sản phẩm 
SELECT * FROM products;
SELECT * FROM cart_items;
SELECT * FROM cart_items;
DELETE FROM products;
DELETE FROM cart_items;
ALTER TABLE products AUTO_INCREMENT = 1;


