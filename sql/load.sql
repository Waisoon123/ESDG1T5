# drop all databases (testing purpose)
# drop database if exists customer_manager;
# drop database if exists product_manager;
# drop database if exists inventory_manager;
# drop database if exists reservation_manager;


# Customer Manager Database
drop database if exists customer_manager;
create database customer_manager;
use customer_manager;

create table `customer_manager` (
	`custID` int(11) NOT NULL AUTO_INCREMENT,
	`name` varchar(256) NOT NULL,
	`gender` varchar(6) NOT NULL,
	`email` varchar(256) NOT NULL,
	constraint customer_manager_pk primary key (`custID`)
);

insert into `customer_manager` values(1, 'Wen Hai', 'Male', 'wenhai87p@gmail.com');
insert into `customer_manager` values(2, 'John', 'Male', 'john.doe@gmail.com');

# Product Manager Database
drop database if exists product_manager;
create database product_manager;
use product_manager;

create table `product_manager` (
	`productID` int(11) NOT NULL AUTO_INCREMENT,
	`productName` varchar(256) NOT NULL,
	`images` varchar(256) NOT NULL,
	`productRate` float NOT NULL,
	constraint product_manager_pk primary key (`productID`)
);

insert into `product_manager` values(1, 'Single Room', 'xxx', 100.0);
insert into `product_manager` values(2, 'Double Room', 'xxx', 200.0);
insert into `product_manager` values(3, 'Suite', 'xxx', 300.0);

# Inventory Manager Database
drop database if exists inventory_manager;
create database inventory_manager;
use inventory_manager;

create table `inventory_manager` (
	`date` date NOT NULL,
	`productName` varchar(256) NOT NULL,
	`quantity` int NOT NULL
	# constraint inventory_manager_pk primary key (`date`, `productName`)
);

insert into `inventory_manager` values('2023-03-11', 'Single Room', 200);
insert into `inventory_manager` values('2023-03-11', 'Double Room', 150);
insert into `inventory_manager` values('2023-03-11', 'Suite', 50);
insert into `inventory_manager` values('2023-03-13', 'Single Room', 200);
insert into `inventory_manager` values('2023-03-13', 'Double Room', 150);
insert into `inventory_manager` values('2023-03-13', 'Suite', 50);

# Reservation Manager Database
drop database if exists reservation_manager;
create database reservation_manager;
use reservation_manager;

CREATE TABLE reservation_manager (
    reservationID INT NOT NULL,
    custID INT NOT NULL,
    startDate VARCHAR(256) NOT NULL,
    endDate VARCHAR(256) NOT NULL,
    productID INT NOT NULL,
    quantity INT NOT NULL,
    session_id varchar(256) NULL,
    PRIMARY KEY (reservationID)
);

INSERT INTO reservation_manager (reservationID, custID, startDate, endDate, productID, quantity) 
VALUES 
(1, 1, '2023-03-24', '2023-03-27', 1, 2),
(2, 2, '2023-03-24', '2023-03-29', 2, 1);