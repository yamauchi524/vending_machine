create table stock(
    drink_id INT,
    stock INT,
    created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    update_date DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY(drink_id)
);

/*insert*/
insert into stock(drink_id, stock) values (1, 10);
insert into stock(drink_id, stock) values (2, 30);
insert into stock(drink_id, stock) values (3, 20);

/*定義変更*/
alter table stock modify stock INT UNSIGNED;