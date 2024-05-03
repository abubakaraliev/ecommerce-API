CREATE TABLE IF NOT EXISTS Users (
    id INT(11) NOT NULL AUTO_INCREMENT,
    username VARCHAR(255) UNIQUE DEFAULT NULL,
    email VARCHAR(255) UNIQUE DEFAULT NULL,
    password VARCHAR(255) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS Products (
    id INT(11) NOT NULL AUTO_INCREMENT,
    identifier VARCHAR(255) DEFAULT NULL,
    price VARCHAR(255) DEFAULT NULL,
    is_available TINYINT(1) DEFAULT NULL,
    PRIMARY KEY (id),
    KEY ix_Products_identifier (identifier)
);

CREATE TABLE IF NOT EXISTS userRoles (
    id INT(11) NOT NULL AUTO_INCREMENT,
    user_id INT(11) DEFAULT NULL,
    role VARCHAR(255) DEFAULT NULL,
    PRIMARY KEY (id),
    KEY user_id (user_id),
    KEY ix_userRoles_id (id),
    CONSTRAINT userRoles_ibfk_1 FOREIGN KEY (user_id) REFERENCES Users (id)
);