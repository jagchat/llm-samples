- Used following AI prompt to create shifts generating function:

```
I am using PostgresSQL.  I have following departments generated through following sql:

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

I have following employees generated through following sql:

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

I created employee shift table as below:

        CREATE TABLE shifts.shift_info (
            shift_id        varchar(50)  PRIMARY KEY,
            emp_id          varchar(50) NOT NULL,
            dept_id         varchar(50) NOT NULL,
            start_date      date NOT NULL,
            start_time      time NOT NULL,
            end_date        date NOT NULL,
            end_time        time NOT NULL
        );

I would like to have employee shifts to be created for above departments and employees randomly.  Following are the rules to create data:

- end_date should be greater than start_date (unless past midnight, end_date would be same as start_date)
- end_time should be greater than start_time (unless past midnight)
- if the end_time is past midnight, end_date should change accordingly
- shifts can be 8 hour or 4 hour
- round the start time to nearest 15 min
- employees cannot have overlapping shifts
- the shifts need to be created randomly between 2024-01-01 and 2024-01-31
- every employee should have at least one shift a day between 2024-01-01 and 2024-01-31
- employees can work in any department for a shift
- employees can work in two different shifts in two departments on a same day

Generate a PostgresSQL function based on above rules.
```
