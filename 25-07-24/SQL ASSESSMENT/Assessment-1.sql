create database fitnessTracker;
use fitnessTracker;
-- create tables
create table exercises (
exercise_id int primary key,
exercise_name varchar(50),
category varchar(30),
calories_burn_per_min int
);

create table workoutlog (
log_id int primary key,
exercise_id int,
date date,
duration_min int,
mood varchar(20),
foreign key (exercise_id) references exercises(exercise_id)
);

-- insert data into exercises
insert into exercises values 
(1, 'running', 'cardio', 10),
(2, 'cycling', 'cardio', 8),
(3, 'weight lifting', 'strength', 6),
(4, 'yoga', 'flexibility', 4),
(5, 'jump rope', 'cardio', 12);

-- insert data into workoutlog
insert into workoutlog values
(1, 1, '2025-03-01', 30, 'energized'),
(2, 1, '2025-03-05', 20, 'tired'),
(3, 2, '2025-03-03', 25, 'normal'),
(4, 2, '2025-03-10', 40, 'energized'),
(5, 3, '2025-03-07', 45, 'tired'),
(6, 3, '2025-03-11', 30, 'normal'),
(7, 4, '2025-03-04', 20, 'normal'),
(8, 4, '2025-03-12', 35, 'energized'),
(9, 5, '2025-03-09', 15, 'tired'),
(10, 5, '2025-03-15', 25, 'normal');

-- 1. all cardio exercises
select * from exercises where category = 'cardio';

-- 2. workouts in march 2025
select * from workoutlog 
where month(date) = 3 and year(date) = 2025;

-- 3. total calories burned per workout
select log_id,duration_min,calories_burn_per_min,(duration_min * calories_burn_per_min) as total_calories
from workoutlog w
join exercises e on w.exercise_id = e.exercise_id;

-- 4. average duration per category
select e.category,avg(w.duration_min) as avg_duration
from workoutlog w
join exercises e on w.exercise_id = e.exercise_id
group by e.category;

-- 5. exercise name, date, duration, calories burned
select e.exercise_name,w.date,w.duration_min,(w.duration_min * e.calories_burn_per_min) as calories_burned
from workoutlog w
join exercises e on w.exercise_id = e.exercise_id;

-- 6. total calories burned per day
select w.date,sum(w.duration_min * e.calories_burn_per_min) as total_calories
from workoutlog w
join exercises e on w.exercise_id = e.exercise_id
group by w.date;

-- 7. exercise that burned most total calories
select exercise_name 
from exercises
where exercise_id = (
select w.exercise_id
from workoutlog w
join exercises e on w.exercise_id = e.exercise_id
group by w.exercise_id
order by sum(w.duration_min * e.calories_burn_per_min) desc
limit 1);

-- 8. exercises never logged
select * from exercises 
where exercise_id not in (
select distinct exercise_id from workoutlog);

-- 9. workouts where mood was tired and duration > 30
select * from workoutlog 
where mood = 'tired' and duration_min > 30;

-- 10. correct wrongly entered mood
update workoutlog
set mood = 'normal'
where log_id = 2;

-- 11. update calories for running
update exercises
set calories_burn_per_min = 11
where exercise_name = 'running';

-- 12. delete logs from february 2024
delete from workoutlog
where month(date) = 2 and year(date) = 2024;
