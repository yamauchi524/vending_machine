create table drink(
    drink_id INT AUTO_INCREMENT,
    drink_name VARCHAR(100),
    drink_image MEDIUMBLOB,
    price INT,
    created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    update_date DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    open_status INT,
    PRIMARY KEY(drink_id)
);