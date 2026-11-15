-- Speeds up searches by name: Seq Scan becomes Index Scan.
CREATE INDEX IF NOT EXISTS items_name_idx ON items (name);
ANALYZE items;
