-- Use the correct database
USE CarRentalDB;

-- Insert into Customers
INSERT INTO Customers VALUES
(1, 'John', 'Doe', 'john.doe@example.com', '555-123-4567'),
(2, 'Jane', 'Smith', 'jane.smith@example.com', '555-987-6543'),
(3, 'Alice', 'Johnson', 'alice.j@example.com', '555-222-3333'),
(4, 'Bob', 'Brown', 'bob.b@example.com', '555-444-5555'),
(5, 'Emily', 'Clark', 'emily.c@example.com', '555-777-8888');

-- Insert into Cars
INSERT INTO Cars VALUES
(1, 'Compact', 'Red', 25.00),
(2, 'Truck', 'Blue', 30.00),
(3, 'Sedan', 'Black', 20.00),
(4, 'SUV', 'White', 35.00),
(5, 'Convertible', 'Yellow', 40.00);

-- Insert into Rentals
INSERT INTO Rentals VALUES
(1, 1, 1, '2023-04-01', '2023-04-03'),
(2, 2, 2, '2023-04-02', '2023-04-04'),
(3, 3, 3, '2023-04-05', '2023-04-06'),
(4, 4, 4, '2023-04-06', '2023-04-08'),
(5, 5, 5, '2023-04-07', '2023-04-09'),
(6, 1, 2, '2023-05-01', '2023-05-03'),
(7, 3, 1, '2023-05-04', '2023-05-06');

-- Insert into Invoices
-- Autogenarated by rental data
-- View Customers
SELECT * FROM Customers;
-- View Cars
SELECT * FROM Cars;
-- View Rentals
SELECT * FROM Rentals;
-- View Invoices
SELECT * FROM Invoices;

