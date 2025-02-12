\c maindb

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM pg_catalog.pg_namespace
        WHERE nspname = 'employees'
    ) THEN
        -- Create the schema if it does not exist
        EXECUTE 'CREATE SCHEMA employees';
        RAISE NOTICE 'Schema "employees" created.';
    ELSE
        RAISE NOTICE 'Schema "employees" already exists.';
    END IF;
END
$$;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM pg_catalog.pg_namespace
        WHERE nspname = 'shifts'
    ) THEN
        -- Create the schema if it does not exist
        EXECUTE 'CREATE SCHEMA shifts';
        RAISE NOTICE 'Schema "shifts" created.';
    ELSE
        RAISE NOTICE 'Schema "shifts" already exists.';
    END IF;
END
$$;