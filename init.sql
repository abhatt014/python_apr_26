-- Single shared database for all services.
-- Each service still only queries its own table(s) in code (auth-service ->
-- users, product-service -> products, order-service -> orders) — sharing
-- one physical database is just a deployment simplification, not a change
-- to which service is allowed to touch what.

CREATE TABLE users (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY (email)
);

CREATE TABLE products (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    name VARCHAR(150) NOT NULL,
    price DECIMAL(10,2) UNSIGNED NOT NULL,
    stock INT UNSIGNED NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- Now that everything lives in one database, the foreign keys back to
-- users/products can be restored (they weren't possible across separate
-- per-service databases). product_name/product_price are still captured
-- at order time so order history keeps showing what was actually paid,
-- even if the product's price changes later.
CREATE TABLE orders (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    user_id INT UNSIGNED NOT NULL,
    product_id INT UNSIGNED NOT NULL,
    product_name VARCHAR(150) NOT NULL,
    product_price DECIMAL(10,2) UNSIGNED NOT NULL,
    total_price DECIMAL(10,2) UNSIGNED NOT NULL DEFAULT 0.00,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    KEY (user_id),
    KEY (product_id),
    CONSTRAINT fk_orders_user_id FOREIGN KEY (user_id) REFERENCES users(id),
    CONSTRAINT fk_orders_product_id FOREIGN KEY (product_id) REFERENCES products(id)
);

-- Seed users. Password for all seed accounts is "123456",
-- stored as a proper salted hash (werkzeug scrypt), not plaintext.
INSERT INTO users (name, email, password) VALUES
('John Doe', 'john@example.com', 'scrypt:32768:8:1$fEE1zI8960KGLq2c$8950e47bb8785a3f477aa7f033d7675f9280d2bb3c416cb1b66838231ecd126ff22a39e4f8867bfb3bfa356bbaf1796f65db835603920e2f69170a063e2e5301'),
('Jane Smith', 'jane@example.com', 'scrypt:32768:8:1$fEE1zI8960KGLq2c$8950e47bb8785a3f477aa7f033d7675f9280d2bb3c416cb1b66838231ecd126ff22a39e4f8867bfb3bfa356bbaf1796f65db835603920e2f69170a063e2e5301'),
('Michael Chen', 'mchen@example.com', 'scrypt:32768:8:1$fEE1zI8960KGLq2c$8950e47bb8785a3f477aa7f033d7675f9280d2bb3c416cb1b66838231ecd126ff22a39e4f8867bfb3bfa356bbaf1796f65db835603920e2f69170a063e2e5301'),
('Sarah Connor', 'connor@example.com', 'scrypt:32768:8:1$fEE1zI8960KGLq2c$8950e47bb8785a3f477aa7f033d7675f9280d2bb3c416cb1b66838231ecd126ff22a39e4f8867bfb3bfa356bbaf1796f65db835603920e2f69170a063e2e5301');

-- Seed products.
INSERT INTO products (name, price, stock) VALUES
('14-inch Business Laptop', 1199.99, 45),
('Wireless Noise-Cancelling Headphones', 199.50, 120),
('Mechanical Ergonomic Keyboard', 129.99, 85),
('27-inch 4K USB-C Monitor', 349.00, 30),
('Wireless Optical Mouse', 24.99, 250);