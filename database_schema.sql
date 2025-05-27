-- Ensure you are in the correct database context before running this.
-- Example: USE grocery_store;

-- Table for Units of Measure
CREATE TABLE IF NOT EXISTS uom (
    uom_id INT AUTO_INCREMENT PRIMARY KEY,
    uom_name VARCHAR(45) NOT NULL UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table for Products
CREATE TABLE IF NOT EXISTS products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    uom_id INT NOT NULL,
    price_per_unit DECIMAL(10, 2) NOT NULL,
    CONSTRAINT fk_products_uom FOREIGN KEY (uom_id) REFERENCES uom(uom_id) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table for Orders
CREATE TABLE IF NOT EXISTS orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    total_cost DECIMAL(10, 2) NOT NULL, -- Matches column name used in orders_dao.py
    datetime DATETIME NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table for Order Details (linking Orders and Products)
CREATE TABLE IF NOT EXISTS order_details (
    order_detail_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity DECIMAL(10, 2) NOT NULL,
    total_price DECIMAL(10, 2) NOT NULL,
    CONSTRAINT fk_order_details_order FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_order_details_product FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Seed Data (Essential for frontend functionality and basic testing)

-- Insert UOMs
INSERT IGNORE INTO uom (uom_id, uom_name) VALUES (1, 'each');
INSERT IGNORE INTO uom (uom_id, uom_name) VALUES (2, 'kg');
INSERT IGNORE INTO uom (uom_id, uom_name) VALUES (3, 'litre');
INSERT IGNORE INTO uom (uom_id, uom_name) VALUES (4, 'dozen');
INSERT IGNORE INTO uom (uom_id, uom_name) VALUES (5, 'gm');

-- Insert a sample product with product_id = 1
-- This is referenced by the default order details in index.html
INSERT IGNORE INTO products (product_id, name, uom_id, price_per_unit) VALUES (1, 'Sample Banana', 1, 0.75);
INSERT IGNORE INTO products (product_id, name, uom_id, price_per_unit) VALUES (2, 'Organic Apples', 2, 3.99);
INSERT IGNORE INTO products (product_id, name, uom_id, price_per_unit) VALUES (3, 'Milk', 3, 2.50);

-- You can add more sample products if you wish:
-- INSERT IGNORE INTO products (name, uom_id, price_per_unit) VALUES ('Whole Wheat Bread', 1, 3.00);
-- INSERT IGNORE INTO products (name, uom_id, price_per_unit) VALUES ('Orange Juice', 3, 4.50);