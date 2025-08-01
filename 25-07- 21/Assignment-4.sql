-- Database creation
create database movie_rentalstoredb;
use movie_rentalstoredb;

-- Schema creation
-- movies table
create table movies (
  movie_id int primary key,
  title varchar(100),
  genre varchar(50),
  release_year year,
  rental_rate decimal(6,2)
);
-- customers table
create table customers(
  customer_id int primary key,
  name varchar(100),
  email varchar(100) unique,
  city varchar(50)
);

-- rentals table
create table rentals (
  rental_id int primary key,
  customer_id int,
  movie_id int,
  rental_date date,
  return_date date,
  foreign key (customer_id) references customers(customer_id) on delete cascade,
  foreign key (movie_id) references movies(movie_id)on delete cascade
);

-- Inserting records
insert into movies values
(1, 'Life of pi', 'Documentary', 2010, 120.00),
(2, 'Hellen keller', 'Biography', 2020, 80.00),
(3, 'War', 'Action', 2023, 150.00),
(4, 'okok', 'Comedy', 2009, 90.00),
(5, 'Interstellar', 'Sci-Fi', 2014, 130.00);

insert into customers values
(1, 'sowgenya', 'sow@gmail.com', 'chennai'),
(2, 'keerthi', 'kk@gmail.com', 'Mumbai'),
(3, 'Rajeev', 'raj@gmail.com', 'kolkatta'),
(4, 'Snehan', 'snehan@gmail.com', 'Hyderabad'),
(5, 'Rohit', 'rohit@gmail.com', 'Chennai'),
(6,'Amit Sharma','amit@gmail.com','Bangalore');

insert into rentals values
(1, 1, 1, '2024-05-02', '2024-05-05'),  
(2, 1, 3, '2024-06-01', '2024-06-09'),  
(3, 2, 2, '2024-07-10', '2024-07-12'),
(4, 3, 4, '2024-06-15', null),        
(5, 3, 1, '2024-06-18', '2024-06-20'),
(6, 4, 5, '2024-06-20', '2024-06-23'),
(7, 2, 3, '2024-06-25', null),         
(8, 1, 1, '2024-07-01', '2024-07-03'),
(9,6,2,'2024-06-09','2024-06-10');


-- SECTION 3: Query Execution
-- Basic Queries

-- 1. Retrieve all movies rented by a customer named 'Amit Sharma'.
select m.title
from rentals r
join customers c on r.customer_id = c.customer_id
join movies m on r.movie_id = m.movie_id
where c.name = 'Amit Sharma';
-- 2. Show the details of customers from 'Bangalore'.
select * from customers
where city = 'Bangalore';

-- 3. List all movies released after the year 2020.
select * from movies
where release_year > 2020;

-- Aggregate Queries
-- 4. Count how many movies each customer has rented.
select name, count(*) as total_rentals
from customers c
join rentals r on c.customer_id = r.customer_id
group by name;

-- 5. Find the most rented movie title.
select title, count(*) as times_rented from movies m
join rentals r on m.movie_id = r.movie_id
group by title
order by times_rented desc
limit 1;

-- 6. Calculate total revenue earned from all rentals.
select sum(rental_rate) as total_revenue
from rentals r
join movies m on r.movie_id = m.movie_id;

-- Advanced Queries
-- 7. List all customers who have never rented a movie.
select name from customers
where customer_id not in (select  customer_id from rentals);

-- 8. Show each genre and the total revenue from that genre.
select m.genre, sum(m.rental_rate) as revenue
from rentals r
join movies m on r.movie_id = m.movie_id
group by m.genre;

-- 9. Find the customer who spent the most money on rentals.
select name, sum(rental_rate) as total_spent
from rentals r
join customers c on r.customer_id = c.customer_id
join movies m on r.movie_id = m.movie_id
group by name
order by total_spent desc
limit 1;

-- 10. Display movie titles that were rented and not yet returned ( return_date IS NULL ).
select title
from rentals r
join movies m on r.movie_id = m.movie_id
where return_date is null;


