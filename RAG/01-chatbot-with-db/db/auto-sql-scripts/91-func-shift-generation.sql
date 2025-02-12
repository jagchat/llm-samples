\c maindb

-- AI generated - may have bugs (check readme.md to tune this further)
CREATE OR REPLACE FUNCTION shifts.generate_random_shifts()
RETURNS void AS $$
DECLARE
    v_current_date date;
    v_emp_record RECORD;
    v_dept_array varchar[] := ARRAY['sales', 'front-desk', 'maintenance', 'training'];
    v_shift_duration interval;
    v_shift_id varchar(50);
    v_start_time time;
    v_end_time time;
    v_end_date date;
    v_attempt_count integer;
    v_shift_count integer;
    v_start_timestamp timestamp;
    v_end_timestamp timestamp;
    v_random_minutes integer;
BEGIN
    -- Clear existing shifts
    DELETE FROM shifts.shift_info;
    
    -- Loop through each day in January 2024
    v_current_date := '2024-06-01'::date;
    
    WHILE v_current_date <= '2025-06-30'::date LOOP
        -- For each employee
        FOR v_emp_record IN SELECT emp_id FROM employees.employee_info LOOP
            -- Ensure at least one shift per day
            v_shift_count := 0;
            v_attempt_count := 0;
            
            WHILE v_shift_count < 1 AND v_attempt_count < 10 LOOP
                -- Randomly decide shift duration (4 or 8 hours)
                v_shift_duration := CASE WHEN random() < 0.5 THEN interval '4 hours' ELSE interval '8 hours' END;
                
                -- Generate random start time between 00:00 and 20:00
                -- First get total random minutes (0 to 1200 minutes = 20 hours)
                v_random_minutes := floor(random() * 1200);
                -- Round to nearest 15 minutes
                v_random_minutes := round(v_random_minutes / 15) * 15;
                -- Convert to hours and minutes
                v_start_timestamp := v_current_date + 
                                   (floor(v_random_minutes / 60)::text || ' hours')::interval + 
                                   ((v_random_minutes % 60)::text || ' minutes')::interval;
                v_start_time := v_start_timestamp::time;
                
                -- Calculate end timestamp and extract time and date
                v_end_timestamp := v_start_timestamp + v_shift_duration;
                v_end_time := v_end_timestamp::time;
                v_end_date := v_end_timestamp::date;
                
                -- Check for overlap with existing shifts
                IF NOT EXISTS (
                    SELECT 1 
                    FROM shifts.shift_info s
                    WHERE s.emp_id = v_emp_record.emp_id
                    AND (
                        TIMESTAMP WITH TIME ZONE 'epoch' + 
                        (EXTRACT(EPOCH FROM (v_current_date + v_start_time::interval)) * INTERVAL '1 second'),
                        TIMESTAMP WITH TIME ZONE 'epoch' + 
                        (EXTRACT(EPOCH FROM (v_end_date + v_end_time::interval)) * INTERVAL '1 second')
                    ) OVERLAPS (
                        TIMESTAMP WITH TIME ZONE 'epoch' + 
                        (EXTRACT(EPOCH FROM (s.start_date + s.start_time::interval)) * INTERVAL '1 second'),
                        TIMESTAMP WITH TIME ZONE 'epoch' + 
                        (EXTRACT(EPOCH FROM (s.end_date + s.end_time::interval)) * INTERVAL '1 second')
                    )
                ) THEN
                    -- Generate unique shift_id
                    v_shift_id := v_emp_record.emp_id || '_' || 
                                 to_char(v_current_date, 'YYYYMMDD') || '_' ||
                                 to_char(v_start_time, 'HH24MI');
                    
                    -- Insert the shift
                    INSERT INTO shifts.shift_info (
                        shift_id, emp_id, dept_id, 
                        start_date, start_time, 
                        end_date, end_time
                    )
                    VALUES (
                        v_shift_id,
                        v_emp_record.emp_id,
                        v_dept_array[1 + floor(random() * array_length(v_dept_array, 1))],
                        v_current_date,
                        v_start_time,
                        v_end_date,
                        v_end_time
                    );
                    
                    v_shift_count := v_shift_count + 1;
                END IF;
                
                v_attempt_count := v_attempt_count + 1;
            END LOOP;
            
            -- Randomly add a second shift with 30% probability
            IF random() < 0.3 THEN
                v_attempt_count := 0;
                
                WHILE v_attempt_count < 10 LOOP
                    v_shift_duration := interval '4 hours'; -- Second shifts are always 4 hours
                    
                    -- Generate random start time between 00:00 and 20:00 rounded to 15 minutes
                    v_random_minutes := floor(random() * 1200);
                    v_random_minutes := round(v_random_minutes / 15) * 15;
                    v_start_timestamp := v_current_date + 
                                       (floor(v_random_minutes / 60)::text || ' hours')::interval + 
                                       ((v_random_minutes % 60)::text || ' minutes')::interval;
                    v_start_time := v_start_timestamp::time;
                    
                    -- Calculate end timestamp and extract time and date
                    v_end_timestamp := v_start_timestamp + v_shift_duration;
                    v_end_time := v_end_timestamp::time;
                    v_end_date := v_end_timestamp::date;
                    
                    -- Check for overlap with existing shifts
                    IF NOT EXISTS (
                        SELECT 1 
                        FROM shifts.shift_info s
                        WHERE s.emp_id = v_emp_record.emp_id
                        AND (
                            TIMESTAMP WITH TIME ZONE 'epoch' + 
                            (EXTRACT(EPOCH FROM (v_current_date + v_start_time::interval)) * INTERVAL '1 second'),
                            TIMESTAMP WITH TIME ZONE 'epoch' + 
                            (EXTRACT(EPOCH FROM (v_end_date + v_end_time::interval)) * INTERVAL '1 second')
                        ) OVERLAPS (
                            TIMESTAMP WITH TIME ZONE 'epoch' + 
                            (EXTRACT(EPOCH FROM (s.start_date + s.start_time::interval)) * INTERVAL '1 second'),
                            TIMESTAMP WITH TIME ZONE 'epoch' + 
                            (EXTRACT(EPOCH FROM (s.end_date + s.end_time::interval)) * INTERVAL '1 second')
                        )
                    ) THEN
                        -- Generate unique shift_id
                        v_shift_id := v_emp_record.emp_id || '_' || 
                                     to_char(v_current_date, 'YYYYMMDD') || '_' ||
                                     to_char(v_start_time, 'HH24MI');
                        
                        -- Insert the shift with a different department
                        INSERT INTO shifts.shift_info (
                            shift_id, emp_id, dept_id, 
                            start_date, start_time, 
                            end_date, end_time
                        )
                        VALUES (
                            v_shift_id,
                            v_emp_record.emp_id,
                            (
                                SELECT dept_id 
                                FROM unnest(v_dept_array) dept_id 
                                WHERE dept_id NOT IN (
                                    SELECT dept_id 
                                    FROM shifts.shift_info 
                                    WHERE emp_id = v_emp_record.emp_id 
                                    AND start_date = v_current_date
                                )
                                ORDER BY random()
                                LIMIT 1
                            ),
                            v_current_date,
                            v_start_time,
                            v_end_date,
                            v_end_time
                        );
                        
                        EXIT;
                    END IF;
                    
                    v_attempt_count := v_attempt_count + 1;
                END LOOP;
            END IF;
        END LOOP;
        
        v_current_date := v_current_date + interval '1 day';
    END LOOP;
END;
$$ LANGUAGE plpgsql;