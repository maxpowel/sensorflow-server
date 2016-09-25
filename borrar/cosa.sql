CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL
);

-- Running upgrade  -> 302abf3f73b4

ALTER TABLE sensor_measure MODIFY magnitude_id INTEGER(11) NOT NULL;

ALTER TABLE sensor_measure MODIFY sensor_id INTEGER(11) NOT NULL;

INSERT INTO alembic_version (version_num) VALUES ('302abf3f73b4');

