DROP TABLE meetings;
DROP TABLE tasks;


CREATE TABLE meetings (
 desc TEXT not null, 
 locat TEXT not null, 
 datetime varchar(32),
 meeting_key INTEGER PRIMARY KEY AUTOINCREMENT
);

CREATE TABLE tasks (
  desc TEXT not Null,
  c_date varchar(32),
  d_date varchar(32),
  a_date varchar(32) not Null,
  assi_to varchar(32),
  task_key INTEGER PRIMARY KEY AUTOINCREMENT
);
