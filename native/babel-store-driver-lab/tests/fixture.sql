CREATE SCHEMA driver_lab;
CREATE TABLE driver_lab.records(id bigint PRIMARY KEY, label text NOT NULL UNIQUE CHECK(octet_length(label)<=256));
CREATE TABLE driver_lab.journal(id bigint PRIMARY KEY REFERENCES driver_lab.records(id) DEFERRABLE INITIALLY DEFERRED);
GRANT USAGE ON SCHEMA driver_lab TO babel_driver_lab;
GRANT SELECT,INSERT,UPDATE,DELETE ON ALL TABLES IN SCHEMA driver_lab TO babel_driver_lab;
