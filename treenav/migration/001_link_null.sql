BEGIN;
ALTER TABLE treenav_menuitem ALTER COLUMN link SET NOT NULL;
COMMIT;
