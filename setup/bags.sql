-- Code to enable referential integrity
PRAGMA foreign_keys = 1;


DROP TABLE IF EXISTS tbl_purchs_items;
DROP TABLE IF EXISTS tbl_purchs;
DROP TABLE IF EXISTS tbl_filters;
drop table if exists tbl_filters_names;
DROP TABLE IF EXISTS tbl_items;
DROP TABLE IF EXISTS tbl_users;
-- Delete the tables if they already exist so that I can easily edit entities.

CREATE TABLE tbl_users(
  	id INTEGER,
  	username VARCHAR(50),
  	email VARCHAR(200),
  	phone INTEGER,
  	password VARCHAR(50),
  	role VARCHAR(50),
  	PRIMARY KEY (id)
);

INSERT INTO tbl_users (id, username, email, phone, password, role) VALUES(1,'oscarwalsdorf','o.walsdorf@stpauls.school.nz',0277771509,'password2','admin');
INSERT INTO tbl_users (id, username, email, phone, password, role) VALUES(2,'jamessu','jsu2@stpauls.school.nz',0221876075,'password3','user');
INSERT INTO tbl_users (id, username, email, phone, password, role) VALUES(3,'liamstiles','lstiles@stpauls.school.nz',0214928735,'password4','admin');
INSERT INTO tbl_users (id, username, email, phone, password, role) VALUES(4,'ryaningram','ringram@stpauls.school.nz',0277310822,'password5','user');

CREATE TABLE tbl_items(
  	id INTEGER,
	name VARCHAR(50),
  	cost FLOAT,
  	image BLOB,
  	stock INT,
    PRIMARY KEY (id)
);

INSERT INTO tbl_items (id, name, cost, image, stock) VALUES(1,'Tramping Bag',200,'img.png',20);
INSERT INTO tbl_items (id, name, cost, image, stock) VALUES(2,'Pack Liner',15,'img.png',70);
INSERT INTO tbl_items (id, name, cost, image, stock) VALUES(3,'Sleeping Bag',125,'img.png',30);
INSERT INTO tbl_items (id, name, cost, image, stock) VALUES(4,'Roll Mat',40,'img.png',25);
INSERT INTO tbl_items (id, name, cost, image, stock) VALUES(5,'Rain Jacket',100,'img.png',80);


CREATE table tbl_filters_names(
  id INTEGER,
  name varchar(50),
  primary key(id)
);
INSERT INTO tbl_filters_names (id, name) VALUES(1, 'Essential');
INSERT INTO tbl_filters_names (id, name) VALUES(2, 'Popular');
INSERT INTO tbl_filters_names (id, name) VALUES(3, 'Clothing');



CREATE TABLE tbl_filters(
	id INTEGER,
  	name_id INTEGER,
    PRIMARY KEY(id, name_id),
  	FOREIGN KEY(id) REFERENCES tbl_items(id),
  	FOREIGN Key(name_id) references tbl_filters_names(id)
);
INSERT INTO tbl_filters (id, name_id) VALUES(1,1);
INSERT INTO tbl_filters (id, name_id) VALUES(1,2);
INSERT INTO tbl_filters (id, name_id) VALUES(2,1);
INSERT INTO tbl_filters (id, name_id) VALUES(3,1);
INSERT INTO tbl_filters (id, name_id) VALUES(3,2);
INSERT INTO tbl_filters (id, name_id) VALUES(4,1);
INSERT INTO tbl_filters (id, name_id) VALUES(5,1);
INSERT INTO tbl_filters (id, name_id) VALUES(5,3);
INSERT INTO tbl_filters (id, name_id) VALUES(5,2);


CREATE TABLE tbl_purchs(
    id INTEGER,
    total FLOAT,
    sale_date DATETIME,
  	user VARCHAR(200),
    PRIMARY KEY(id),
  	FOREIGN KEY(user) REFERENCES tbl_users(id)
);

INSERT INTO tbl_purchs (id, total, sale_date, user) VALUES(1,0,'2024-04-03 18:41:15',1);
INSERT INTO tbl_purchs (id, total, sale_date, user) VALUES(2,0,'2024-04-03 19:21:31',2);
INSERT INTO tbl_purchs (id, total, sale_date, user) VALUES(3,0,'2024-04-03 13:12:08',3);


CREATE TABLE tbl_purchs_items(
    purchase_id INTEGER,
    item_id INTEGER,
    quantity INT,
    PRIMARY KEY(purchase_id, item_id),
    FOREIGN KEY(purchase_id) REFERENCES tbl_purchs(id),
    FOREIGN KEY(item_id) REFERENCES tbl_items(id)
);

INSERT INTO tbl_purchs_items (purchase_id, item_id, quantity) VALUES(1,1,1);
INSERT INTO tbl_purchs_items (purchase_id, item_id, quantity) VALUES(1,2,2);
INSERT INTO tbl_purchs_items (purchase_id, item_id, quantity) VALUES(1,3,1);
INSERT INTO tbl_purchs_items (purchase_id, item_id, quantity) VALUES(2,4,1);
INSERT INTO tbl_purchs_items (purchase_id, item_id, quantity) VALUES(3,5,2);
INSERT INTO tbl_purchs_items (purchase_id, item_id, quantity) VALUES(3,1,1);
INSERT INTO tbl_purchs_items (purchase_id, item_id, quantity) VALUES(3,2,1);
INSERT INTO tbl_purchs_items (purchase_id, item_id, quantity) VALUES(3,3,1);