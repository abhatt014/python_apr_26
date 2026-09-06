-- Create users table
CREATE TABLE users (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY (email)
);

-- Create products table
CREATE TABLE products (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    name VARCHAR(150) NOT NULL,
    price DECIMAL(10,2) UNSIGNED NOT NULL,
    stock INT UNSIGNED NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- Create orders table
CREATE TABLE orders (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    user_id INT UNSIGNED NOT NULL,
    product_id INT UNSIGNED NOT NULL,
    total_price DECIMAL(10,2) UNSIGNED NOT NULL DEFAULT 0.00,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    KEY (user_id),
    KEY (product_id),
    CONSTRAINT fk_orders_user_id FOREIGN KEY (user_id) REFERENCES users(id),
    CONSTRAINT fk_orders_product_id FOREIGN KEY (product_id) REFERENCES products(id)
);


-- Insert sample data into users table
-- Passwords are represented as plain text/dummy hashes for demonstration purposes
INSERT INTO users (name, email, password) VALUES
('John Doe', 'john@example.com', '123456'),
('Jane Smith', 'jane@example.com', '123456'),
('Michael Chen', 'mchen@example.com', '123456'),
('Sarah Connor', 'connor@example.com', '123456');

-- Insert sample data into products table
INSERT INTO products (name, price, stock) VALUES
('14-inch Business Laptop', 1199.99, 45),
('Wireless Noise-Cancelling Headphones', 199.50, 120),
('Mechanical Ergonomic Keyboard', 129.99, 85),
('27-inch 4K USB-C Monitor', 349.00, 30),
('Wireless Optical Mouse', 24.99, 250);