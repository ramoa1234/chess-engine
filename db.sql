CREATE TABLE tree_adj (
  id int(10) unsigned NOT NULL AUTO_INCREMENT,
  parent_id int(10) unsigned DEFAULT NULL,
  title varchar(255) NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (parent_id) REFERENCES tree_adj (id) 
    ON DELETE CASCADE ON UPDATE CASCADE
);
