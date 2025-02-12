\c maindb

DO $$
BEGIN
    IF EXISTS (SELECT 1 
                FROM information_schema.tables 
                WHERE table_name = 'shift_info'
                AND table_schema = 'shifts') THEN
		RAISE NOTICE 'Table "shifts.shift_info" already exists.';
	ELSE
        RAISE NOTICE 'Table "shifts.shift_info": Creating..';
        CREATE TABLE shifts.shift_info (
            seq_id              SERIAL UNIQUE,
            shift_id            varchar(50) PRIMARY KEY,
            emp_id              varchar(50) NOT NULL,
            dept_id             varchar(50) NOT NULL,
            start_date          date NOT NULL,
            start_time          time NOT NULL,
            end_date            date NOT NULL,
            end_time            time NOT NULL,
            created_at          timestamp DEFAULT CURRENT_TIMESTAMP
        );
        RAISE NOTICE 'Table "shifts.shift_info": Completed';
    END IF;
END $$;
