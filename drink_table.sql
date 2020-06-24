create table drink(
    drink_id INT AUTO_INCREMENT,
    name VARCHAR(100),
    image VARCHAR(255),
    price INT,
    created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    update_date DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    status INT,
    PRIMARY KEY(drink_id)
);

/*insert*/
insert into drink(drink_id, name, price, image) values (1, "コーラ", 100, "cola.png");
insert into drink(drink_id, name, price, image) values (2, "ソーダ", 150, "bottle_blue.png");
insert into drink(drink_id, name, price, image) values (3, "ピーチ", 100, "juice.png");