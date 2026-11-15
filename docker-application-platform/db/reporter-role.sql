-- A read-only login for reports: it can look at items, not change them.
-- The password comes in from the command line as the variable pw.
CREATE ROLE reporter LOGIN PASSWORD :'pw';
GRANT CONNECT ON DATABASE items TO reporter;
GRANT USAGE ON SCHEMA public TO reporter;
GRANT SELECT ON items TO reporter;
