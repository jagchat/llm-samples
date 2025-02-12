\c maindb


INSERT INTO employees.dept_info
(dept_id, dept_name)
VALUES('sales', 'Sales');

INSERT INTO employees.dept_info
(dept_id, dept_name)
VALUES('front-desk', 'Front Desk');

INSERT INTO employees.dept_info
(dept_id, dept_name)
VALUES('maintenance', 'Maintenance');

INSERT INTO employees.dept_info
(dept_id, dept_name)
VALUES('training', 'Training');

INSERT INTO employees.employee_info
(emp_id, first_name, last_name, email)
VALUES('1001', 'John', 'Doe', 'john.doe@example.com');

INSERT INTO employees.employee_info
(emp_id, first_name, last_name, email)
VALUES('1002', 'Jane', 'Doe', 'jane.doe@example.com');

INSERT INTO employees.employee_info
(emp_id, first_name, last_name, email)
VALUES('1003', 'Bob', 'Smith', 'bob.smith@example.com');

INSERT INTO employees.employee_info
(emp_id, first_name, last_name, email)
VALUES('1004', 'Alice', 'Johnson', 'alice.johnson@example.com');

INSERT INTO employees.employee_info
(emp_id, first_name, last_name, email)
VALUES('1005', 'Scott', 'Brown', 'scott.brown@example.com');

INSERT INTO employees.employee_info
(emp_id, first_name, last_name, email)
VALUES('1006', 'Peter', 'Parker', 'peter.parker@example.com');

INSERT INTO employees.employee_info
(emp_id, first_name, last_name, email)
VALUES('1007', 'Emma', 'Williams', 'emma.williams@example.com');

INSERT INTO employees.employee_info
(emp_id, first_name, last_name, email)
VALUES('1008', 'Michael', 'Brown', 'michael.brown@example.com');

-- Insert shifts for employee 1001
INSERT INTO shifts.shift_info
(shift_id, emp_id, dept_id, start_date, start_time, end_date, end_time)
VALUES('1001-1', '1001', 'sales', '2024-06-01', '08:00:00', '2024-06-01', '17:00:00');