create table drink_table(
    drink_id INT AUTO_INCREMENT,
    drink_name VARCHAR(100),
    drink_image MEDIUMBLOB,
    price INT,
    created_date DATETIME,
    update_date DATETIME,
    open_status INT,
    PRIMARY KEY(drink_id)
);