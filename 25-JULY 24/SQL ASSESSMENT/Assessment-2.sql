create database travelPlanner;
use travelPlanner;
-- create tables
create table destinations (
destination_id int primary key,
city varchar(100),
country varchar(100),
category varchar(50),
avg_cost_per_day int);

create table trips (
trip_id int primary key,
destination_id int,
traveler_name varchar(100),
start_date date,
end_date date,
budget int,
foreign key (destination_id) references destinations(destination_id));

-- insert sample data
insert into destinations values
(1, 'goa', 'india', 'beach', 2500),
(2, 'jaipur', 'india', 'historical', 2000),
(3, 'bali', 'indonesia', 'beach', 4000),
(4, 'paris', 'france', 'historical', 7000),
(5, 'zurich', 'switzerland', 'nature', 8000),
(6, 'queenstown', 'new zealand', 'adventure', 7500);

insert into trips values
(1, 1, 'arun', '2025-01-10', '2025-01-15', 15000),
(2, 2, 'neha', '2025-03-01', '2025-03-10', 22000),
(3, 3, 'rahul', '2025-02-15', '2025-02-18', 12000),
(4, 4, 'anita', '2025-04-10', '2025-04-17', 50000),
(5, 1, 'arun', '2025-05-05', '2025-05-07', 8000),
(6, 5, 'mohan', '2024-12-10', '2024-12-20', 60000),
(7, 6, 'neha', '2025-06-01', '2025-06-08', 56000),
(8, 2, 'simran', '2025-03-20', '2025-03-25', 15000),
(9, 4, 'rahul', '2023-08-10', '2023-08-14', 35000),
(10, 3, 'anita', '2025-07-01', '2025-07-05', 18000);

-- 1. show all trips to destinations in "india"
select * from trips
where destination_id in (select destination_id from destinations where country = 'india');

-- 2. list all destinations with an average cost below 3000
select * from destinations where avg_cost_per_day < 3000;

-- 3. calculate the number of days for each trip
select trip_id, traveler_name, datediff(end_date, start_date) as duration_days from trips;

-- 4. list all trips that last more than 7 days
select * from trips
where datediff(end_date, start_date) > 7;

-- 5. list traveler name, destination city, and total trip cost (duration × avg_cost_per_day)
select t.traveler_name, d.city,
datediff(t.end_date, t.start_date) * d.avg_cost_per_day as total_trip_cost
from trips t
join destinations d on t.destination_id = d.destination_id;

-- 6. find the total number of trips per country
select d.country, count(*) as total_trips
from trips t
join destinations d on t.destination_id = d.destination_id
group by d.country;

-- 7. show average budget per country
select d.country, avg(t.budget) as avg_budget
from trips t
join destinations d on t.destination_id = d.destination_id
group by d.country;

-- 8. find which traveler has taken the most trips
select traveler_name, count(*) as trips_count
from trips
group by traveler_name
order by trips_count desc
limit 1;

-- 9. show destinations that haven't been visited yet
select * from destinations
where destination_id not in (select distinct destination_id from trips);

-- 10. find the trip with the highest cost per day
select t.*, d.city, d.country,(t.budget / datediff(t.end_date, t.start_date)) as cost_per_day
from trips t
join destinations d on t.destination_id = d.destination_id
order by cost_per_day desc
limit 1;

-- 11. update the budget for a trip that was extended by 3 days
update trips
set budget = budget + (3 * (select avg_cost_per_day from destinations 
where destinations.destination_id = trips.destination_id))where trip_id = 102;

-- 12. delete all trips that were completed before jan 1, 2023
delete from trips
where end_date < '2023-01-01';
