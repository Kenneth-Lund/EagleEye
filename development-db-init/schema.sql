CREATE TABLE processes (
    process_id INT PRIMARY KEY,
    data_count int,
    time_started DATE
);

CREATE TABLE data_table
(
  data_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  process_id int,
  data_value VARCHAR(500),
  data_type VARCHAR(500),
  data_source VARCHAR(500),
  time_retrieved DATE
);