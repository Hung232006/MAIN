USE products;

CREATE TABLE IF NOT EXISTS products (
    productCode VARCHAR(15) NOT NULL PRIMARY KEY,
    productName VARCHAR(70) NOT NULL,
	buyPrice DOUBLE NOT NULL,
    productDescription TEXT NOT NULL,
    FOREIGN KEY (productLine) REFERENCES productlines(productLine)
);

show tables;
select * from products;