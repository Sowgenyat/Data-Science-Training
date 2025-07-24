CREATE DATABASE employeeAttendanceDB;
USE employeeAttendanceDB;
create table employees (
  employee_id int primary key,
  name varchar(100),
  department varchar(50),
  designation varchar(50)
);

create table attendance (
  attendance_id int primary key auto_increment,
  employee_id int,
  clock_in datetime,
  clock_out datetime,
  foreign key (employee_id) references employees(employee_id)
);

create table tasks (
  task_id int primary key auto_increment,
  employee_id int,
  task_description varchar(255),
  task_date date,
  status varchar(50),
  foreign key (employee_id) references employees(employee_id)
);
-- insert a new employee
insert into employees values (1, 'arun', 'hr', 'analyst');

-- insert clock-in/out
insert into attendance (employee_id, clock_in, clock_out)
values (1, '2025-07-24 09:00:00', '2025-07-24 17:30:00');

-- insert task
insert into tasks (employee_id, task_description, task_date, status)
values (1, 'updated employee database', '2025-07-24', 'completed');

delimiter //
create procedure total_hours_by_employee(IN emp_id int)
begin
  select employee_id, 
         sum(timestampdiff(minute, clock_in, clock_out)) / 60 as total_hours
  from attendance
  where employee_id = emp_id
  group by employee_id;
end //
delimiter ;
