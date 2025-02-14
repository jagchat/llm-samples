\c maindb

DO $$
BEGIN
    IF EXISTS (SELECT 1 
                FROM information_schema.tables 
                WHERE table_name = 'dept_info'
                AND table_schema = 'employees') THEN
		RAISE NOTICE 'Table "employees.dept_info" already exists.';
	ELSE
        RAISE NOTICE 'Table "employees.dept_info": Creating..';
        CREATE TABLE employees.dept_info (
            dept_id         varchar(50)  PRIMARY KEY,
            dept_name       varchar(500) NOT NULL
        );
        RAISE NOTICE 'Table "employees.dept_info": Completed';
    END IF;
END $$;
