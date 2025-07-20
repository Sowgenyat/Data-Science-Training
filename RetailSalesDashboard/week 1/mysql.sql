-- Database Creation
CREATE DATABASE  retail_sales;
USE retail_sales;

-- products table
CREATE TABLE products (
    product_id INT PRIMARY KEY,
    name VARCHAR(100),
    category VARCHAR(50),
    price DECIMAL(10,2),
    cost DECIMAL(10,2)
);

-- stores table
CREATE TABLE stores (
    store_id INT PRIMARY KEY,
    name VARCHAR(100),
    location VARCHAR(100),
    region VARCHAR(50)
);

-- employees table
CREATE TABLE employees (
    emp_id INT PRIMARY KEY,
    name VARCHAR(100),
    role VARCHAR(50),
    store_id INT,
    FOREIGN KEY (store_id) REFERENCES stores(store_id)
);

--  sales table
CREATE TABLE sales (
    sale_id INT PRIMARY KEY,
    product_id INT,
    store_id INT,
    emp_id INT,
    quantity INT,
    sale_date DATE,
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    FOREIGN KEY (store_id) REFERENCES stores(store_id),
    FOREIGN KEY (emp_id) REFERENCES employees(emp_id)
);


INSERT INTO products VALUES
(1, 'Laptop', 'Electronics', 55000, 48000),
(2, 'Mouse', 'Electronics', 700, 500);

INSERT INTO stores VALUES
(1, 'All things', 'Chennai', 'South'),
(2, 'Delhi Mall', 'Delhi', 'North');

INSERT INTO employees VALUES
(1, 'Rohit Kumar', 'Sales Associate', 1),
(2, 'Ankitha', 'Cashier', 2);

INSERT INTO sales VALUES
(1, 1, 1, 1, 3, '2025-07-01'),
(2, 2, 2, 2, 10, '2025-07-01');

-- CRUD Operations
-- Read
SELECT * FROM sales;
-- Update
UPDATE products SET price = 54000 WHERE product_id = 1;
-- Delete
DELETE FROM sales WHERE sale_id = 2;
-- Insert
INSERT INTO sales VALUES (3, 2, 1, 1, 5, '2025-07-02');

-- Stored Procedure for daily sales of a store
DELIMITER //
CREATE PROCEDURE get_daily_sales(IN store INT, IN sale_day DATE)
BEGIN
    SELECT s.store_id, SUM(s.quantity * p.price) AS total_sales
    FROM sales s
    JOIN products p ON s.product_id = p.product_id
    WHERE s.store_id = store AND s.sale_date = sale_day
    GROUP BY s.store_id;
END;
//
DELIMITER ;

-- Indexes
CREATE INDEX idex_product_name ON products(name);
CREATE INDEX index_region ON stores(region);
