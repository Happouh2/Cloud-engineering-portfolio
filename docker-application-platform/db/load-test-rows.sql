-- 500,000 fake items, so a slow search actually shows up.
-- Run this once. Running it again adds another 500,000.
INSERT INTO items (name) SELECT 'item-' || g FROM generate_series(1, 500000) AS g;
ANALYZE items;
SELECT count(*) AS total_rows FROM items;
