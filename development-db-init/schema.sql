CREATE TABLE processes (
    process_id int,
    data_id int,
    time_started DATETIME
);

CREATE TABLE data_table
(
  data_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  data_value VARCHAR(500),
  data_type VARCHAR(500),
  data_source VARCHAR(500),
  time_retrieved DATETIME
);