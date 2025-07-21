-- ASSIGNMENT-1(day1)
-- Task1-Create a Table
create table products(
product_id int primary key,
product_name varchar(30),
category varchar(30),
price decimal(10,2),
stock_quantity int,
added_date date);

-- Task2-Insert Records
insert into products values
(1,'iphone','electronic',100000.00,5,'2025-03-09'),
(2,'mouse','electronic',1000.00,5,'2025-03-04'),
(3,'saree','fashion',1300.00,8,'2025-01-11'),
(4,'shoes','footwear',3000.00,10,'2025-02-13'),
(5,'laptop','electronic',150000.00,3,'2025-06-08');

-- Task 3: Write Queries
-- List all products.
select * from products;
-- Display only product_name and price .
select product_name,price from products;
-- Find products with stock_quantity less than 10.
select * from products where stock_quantity<10;
-- Find products with price between 500 and 2000.
select * from products where price between 500 and 2000;
-- Show products added after 2023-01-01 .
select * from products where added_date>'2023-01-01';

-- List all products whose names start with ‘S’.
select * from products where product_name like 'S%';
-- Show all products that belong to either Electronics or Furniture .
select * from products where category in ('electronic','furniture');

-- Task 4: Update & Delete
-- Update the price of one product.
update products set price=1200 where product_id=2;
-- Increase stock of all products in a specific category by 5.
update products set stock_quantity=(stock_quantity+5) where category='electronic';
-- Delete one product based on its product_id .
delete from products where product_id=2;
-- Delete all products with stock_quantity = 0.
delete from products where stock_quantity=0;


