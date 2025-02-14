\c maindb

DO $$
BEGIN
    IF EXISTS (SELECT 1 
                FROM information_schema.tables 
                WHERE table_name = 'employee_info'
                AND table_schema = 'employees') THEN
		RAISE NOTICE 'Table "employees.employee_info" already exists.';
	ELSE
        RAISE NOTICE 'Table "employees.employee_info": Creating..';
        CREATE TABLE employees.employee_info (
            emp_id                varchar(50)  PRIMARY KEY,
            first_name            varchar(500) NOT NULL,
            last_name             varchar(500) NOT NULL,
            email                 varchar(500)
        );
        RAISE NOTICE 'Table "employees.employee_info": Completed';
    END IF;
END $$;

