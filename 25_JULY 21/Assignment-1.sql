-- Database creation
create database employeedb;
use employeedb;

-- Table creation
-- Employees table
create table employees (
emp_id int primary key,
emp_name varchar(100),
department varchar(50),
salary int,
age int
);

-- Departments table
create table departments (
dept_id int primary key,
dept_name varchar(50),
location varchar(50)
);

-- Inserting records in tables
insert into employees values
(101, 'Amit Sharma', 'Engineering', 60000, 30),
(102, 'Neha Reddy', 'Marketing', 45000, 28),
(103, 'Faizan Ali', 'Engineering', 58000, 32),
(104, 'Divya Mehta', 'HR', 40000, 29),
(105, 'Ravi Verma', 'Sales', 35000, 26);

insert into departments values
(1, 'Engineering', 'Bangalore'),
(2, 'Marketing', 'Mumbai'),
(3, 'HR', 'Delhi'),
(4, 'Sales', 'Chennai');

-- Section A: Basic SQL
-- 1.Display all employees.
select * from employees;

-- 2. Show only emp_name and salary of all employees.
select emp_name,salary from employees;

-- 3. Find employees with a salary greater than 40,000.
select * from employees where salary> 40000;

-- 4. List employees between age 28 and 32 (inclusive).
select * from employees where age between  28 and 32;

-- 5. Show employees who are not in the HR department.
select * from employees where department !='HR';

-- 6. Sort employees by salary in descending order.
select emp_name,salary 
from employees 
order by salary desc;

-- 7. Count the number of employees in the table.
select count(emp_id) as numberofemployees from employees;

-- 8. Find the employee with the highest salary.
select emp_name,salary 
from employees 
order by salary desc
limit  1;

-- Section B: Joins & Aggregations
-- 1. Display employee names along with their department locations (using JOIN).
select emp_name,location from employees e
join departments d
on e.department=d.dept_name;

-- 2. List departments and count of employees in each department.
select dept_name,count(emp_id) from departments d
join employees e
on d.dept_name=e.department
group by dept_name;

-- 3. Show average salary per department.
select dept_name,avg(salary)  from departments d
join employees e
on d.dept_name=e.department
group by dept_name;

-- 4. Find departments that have no employees (use LEFT JOIN).
select dept_name,count(emp_id) from departments d
left join employees e
on d.dept_name=e.department
group by dept_name
having count(emp_id) = 0;


-- 5. Find total salary paid by each department.
select dept_name,sum(salary)  as total_salary from departments d
join employees e
on d.dept_name=e.department
group by dept_name;

-- 6. Display departments with average salary > 45,000.
select dept_name,avg(salary) as average_salary  from departments d
join employees e
on d.dept_name=e.department
group by dept_name
having average_salary>45000;

-- 7. Show employee name and department for those earning more than 50,000.
select emp_name,dept_name from employees e
join departments d
on e.department=d.dept_name
where e.salary>50000;

