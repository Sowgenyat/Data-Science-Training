-- Database creation
create database bookstoredb;
use bookstoredb;

-- Tables
-- Book
create table books(
book_id int primary key,
title varchar (30),
author varchar (30),
genre varchar(20),
price decimal (10,2));

-- Customers
create table customers (
customer_id int primary key,
name varchar(100),
email varchar(100),
city varchar(100)
);

-- Orders
create table orders (
order_id int primary key,
customer_id int,
book_id int,
order_date date,
quantity int,
foreign key (customer_id) references customers(customer_id),
foreign key (book_id) references books(book_id)
);

-- Sample data insertion
insert into books values
(1, 'Computer network','Andrew', 'Education', 950),
(2, 'hellen keller','hellen keller', 'Motivation', 500),
(3, 'Atomic Habits', 'James','Self-help', 220),
(4, 'Power of subconsious mind','Joseph Murray', 'Self-development', 680),
(5, 'The Alchemist','paulo', 'Fiction', 350);

insert into customers values
(1, 'sowgenya', 'sow@gmail.com', 'Hyderabad'),
(2, 'Anuj', 'anuj@gmail.com', 'Madurai'),
(3, 'thahir', 'tah@gmail.com', 'Delhi'),
(4, 'Pooja', 'pooj@gmail.com', 'Hyderabad'),
(5, 'alia', 'alia@gmail.com', 'Mumbai');

insert into orders values
(1, 1, 1, '2024-12-15', 2),
(2, 2, 2, '2024-11-10', 1),
(3, 3, 1, '2024-12-18', 1),
(4, 3, 4, '2023-06-25', 2),
(5, 4, 3, '2024-01-15', 3),
(6, 5, 2, '2023-12-01', 2),
(7, 1, 5, '2024-02-02', 2);

-- PART 3: Write and Execute Queries
-- Basic Queries
-- 1. List all books with price above 500.
select * from books where price>500;

-- 2. Show all customers from the city of ‘Hyderabad’.
select * from customers where city='Hyderabad';

-- 3. Find all orders placed after ‘2023-01-01’.
select * from orders where order_date > 2023-01-01;


-- Joins & Aggregations
-- 4. Show customer names along with book titles they purchased.
select name,title from customers c
join orders o
on o.customer_id=c.customer_id
join books b
on o.book_id=b.book_id;

-- 5. List each genre and total number of books sold in that genre.
select genre,count(quantity) from books b
join orders o on o.book_id=b.book_id
group by genre;

-- 6. Find the total sales amount (price × quantity) for each book.
select title, sum(price * quantity) as total_sales
from books b
join orders o on b.book_id = o.book_id
group by b.title;

-- 7. Show the customer who placed the highest number of orders.
select name,count(order_id) as total_order from customers c
join orders o on c.customer_id=o.customer_id
group by name
order by total_order desc
limit 1;

-- 8. Display average price of books by genre.
select genre,avg(price) from books
group by genre;

-- 9. List all books that have not been ordered.
select b.title
from books b
left join orders o on b.book_id = o.book_id
where o.order_id is null;

-- 10. Show the name of the customer who has spent the most in total.
select c.name, sum(b.price * o.quantity) as total_spent
from customers c
join orders o on c.customer_id = o.customer_id
join books b on o.book_id = b.book_id
group by c.name
order by total_spent desc
limit 1;

