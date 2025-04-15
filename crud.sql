-- Use the correct database
USE CarRentalDB;

-- READ: View all customers
SELECT * FROM Customers;

-- UPDATE: Change rental end date for a specific rental
UPDATE Rentals 
SET rental_end_date = '2023-04-07' 
WHERE rental_id = 1;

-- DELETE: Remove invoices with amount less than 100
DELETE FROM Invoices 
WHERE invoice_amount < 100;

-- CALCULATE TOTAL EARNINGS per car
SELECT 
    Cars.car_id, 
    Cars.car_type, 
    SUM(Invoices.invoice_amount) AS TotalEarnings
FROM Cars
JOIN Rentals ON Rentals.car_id = Cars.car_id
JOIN Invoices ON Invoices.rental_id = Rentals.rental_id
GROUP BY Cars.car_id;

-- CALCULATE TOTAL RENTALS per customer
SELECT 
    Customers.customer_id, 
    Customers.first_name, 
    Customers.last_name, 
    COUNT(*) AS TotalRentals
FROM Rentals
JOIN Customers ON Rentals.customer_id = Customers.customer_id
GROUP BY Customers.customer_id;

-- FIND MOST RENTED CARS
SELECT 
    Cars.car_id, 
    Cars.car_type, 
    COUNT(Rentals.rental_id) AS NumberOfRentals
FROM Cars
JOIN Rentals ON Rentals.car_id = Cars.car_id
GROUP BY Cars.car_id
ORDER BY NumberOfRentals DESC;
