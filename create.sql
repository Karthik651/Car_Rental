-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS CarRentalDB;

-- Use the created database
USE CarRentalDB;

-- Create Customers table
CREATE TABLE IF NOT EXISTS Customers (
    customer_id INT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    phone VARCHAR(15)
    -- Functional Dependency: customer_id -> first_name, last_name, email, phone
);

-- Create Cars table
CREATE TABLE IF NOT EXISTS Cars (
    car_id INT PRIMARY KEY,
    car_type VARCHAR(50),
    car_color VARCHAR(30),
    car_price DECIMAL(6,2)
    -- Functional Dependency: car_id -> car_type, car_color, car_price
);

-- Create Rentals table
CREATE TABLE IF NOT EXISTS Rentals (
    rental_id INT PRIMARY KEY,
    customer_id INT,
    car_id INT,
    rental_start_date DATE,
    rental_end_date DATE,
    -- Functional Dependency: rental_id -> customer_id, car_id, rental_start_date, rental_end_date
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id) ON DELETE CASCADE,
    FOREIGN KEY (car_id) REFERENCES Cars(car_id) ON DELETE CASCADE
);

-- Create Invoices table
CREATE TABLE IF NOT EXISTS Invoices (
    invoice_id INT PRIMARY KEY AUTO_INCREMENT,
    rental_id INT,
    invoice_amount DECIMAL(6,2),
    -- Functional Dependency: invoice_id -> rental_id, invoice_amount
    FOREIGN KEY (rental_id) REFERENCES Rentals(rental_id) ON DELETE CASCADE
);

-- Trigger to auto-generate invoice after rental creation
DELIMITER //

CREATE TRIGGER generate_invoice_after_rental
AFTER INSERT ON Rentals
FOR EACH ROW
BEGIN
    DECLARE daily_rate DECIMAL(6,2);
    DECLARE num_days INT;
    DECLARE total DECIMAL(6,2);

    -- Get the daily rate of the rented car
    SELECT car_price INTO daily_rate FROM Cars WHERE car_id = NEW.car_id;

    -- Calculate number of rental days
    SET num_days = DATEDIFF(NEW.rental_end_date, NEW.rental_start_date);

    -- Calculate total invoice amount
    SET total = daily_rate * num_days;

    -- Insert invoice
    INSERT INTO Invoices (rental_id, invoice_amount) VALUES (NEW.rental_id, total);
END;
//

DELIMITER ;
