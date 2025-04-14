-- Создание таблицы Roles
CREATE TABLE Role (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL
);

-- Создание таблицы Users
CREATE TABLE User (
    id INT PRIMARY KEY AUTO_INCREMENT,
    lastname VARCHAR(50),
    name VARCHAR(50) NOT NULL,
    surname VARCHAR(50),
    role_id INT,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    FOREIGN KEY (role_id) REFERENCES Role(id)
);

-- Создание таблицы Orders
CREATE TABLE `Order` (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    address_from_geo_lat DECIMAL(9, 6),
    address_from_geo_long DECIMAL(9, 6),
    address_to_geo_lat DECIMAL(9, 6),
    address_to_geo_long DECIMAL(9, 6),
    trackers VARCHAR(255),  -- список трекеров через запятую
    invoice_id INT,
    FOREIGN KEY (user_id) REFERENCES User(id),
    FOREIGN KEY (invoice_id) REFERENCES Invoice(id)
);

-- Создание таблицы Invoices
CREATE TABLE Invoice (
    id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT,
    price DECIMAL(10, 2),
    courier_price DECIMAL(10, 2),
    comission DECIMAL(10, 2),
    FOREIGN KEY (order_id) REFERENCES `Order`(id)
);

-- Создание таблицы Trackers
CREATE TABLE Tracker (
    id INT PRIMARY KEY AUTO_INCREMENT,
    courier_id INT,
    order_id INT,
    track_number VARCHAR(50) NOT NULL,
    FOREIGN KEY (courier_id) REFERENCES User(id),
    FOREIGN KEY (order_id) REFERENCES `Order`(id)
);
