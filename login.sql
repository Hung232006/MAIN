
USE login;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nameusers VARCHAR(255) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    pass VARCHAR(255) NOT NULL,
    requestpass VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
show tables;
SELECT * FROM users;
CREATE TABLE CartItems (
    CartItemID INT AUTO_INCREMENT PRIMARY KEY,   -- Khóa chính cho từng dòng sản phẩm
    CartID INT NOT NULL,                         -- Mã giỏ hàng (gắn với người dùng)
    UserID INT NOT NULL,                         -- Người dùng sở hữu giỏ hàng
    ProductID INT NOT NULL,                      -- Mã sản phẩm
    Quantity INT NOT NULL DEFAULT 1,             -- Số lượng sản phẩm
    UnitPrice DECIMAL(10,2) NOT NULL,            -- Giá đơn vị
    TotalPrice DECIMAL(10,2) AS (Quantity * UnitPrice) STORED, -- Thành tiền (tính tự động)
    Status ENUM('Pending','Ordered','Cancelled') DEFAULT 'Pending', -- Trạng thái
    AddedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Thời điểm thêm vào giỏ
    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);


