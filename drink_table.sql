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
insert into drink(drink_id, name, price, image) values (1, "コーラ", 100, "/drink_image/cola.png");
insert into drink(drink_id, name, price, image) values (2, "ソーダ", 150, "/drink_image/bottle_blue.png");
insert into drink(drink_id, name, price, image) values (3, "ピーチ", 100, "/drink_image/juice.png");

/*定義の変更*/
alter table drink modify price INT UNSIGNED;