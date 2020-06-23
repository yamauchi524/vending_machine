create table drink(
    drink_id INT AUTO_INCREMENT,
    name VARCHAR(100),
    image MEDIUMBLOB,
    price INT,
    created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    update_date DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    status INT,
    PRIMARY KEY(drink_id)
);