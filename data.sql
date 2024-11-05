-- Create the Categories Table
create database Preet;
use Preet;
CREATE TABLE IF NOT EXISTS Categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(50) NOT NULL
);

-- Create the Transactions Table
CREATE TABLE IF NOT EXISTS Transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    transaction_date DATE NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    category_id INT,
    description TEXT,
    FOREIGN KEY (category_id) REFERENCES Categories(category_id)
);

-- Insert Sample Data into Categories
INSERT INTO Categories (category_name) VALUES 
    ('Food'), 
    ('Transport'), 
    ('Utilities'), 
    ('Entertainment');

-- Insert Sample Data into Transactions


-- Query to Calculate Monthly Spending
SELECT 
    DATE_FORMAT(transaction_date, '%Y-%m') AS month, 
    SUM(amount) AS total_spent
FROM 
    Transactions
GROUP BY 
    month
ORDER BY 
    month DESC;

-- Query to Calculate Spending Breakdown by Category for a Given Month (e.g., '2024-11')
SELECT 
    c.category_name, 
    SUM(t.amount) AS total_spent
FROM 
    Transactions t
JOIN 
    Categories c ON t.category_id = c.category_id
WHERE 
    DATE_FORMAT(t.transaction_date, '%Y-%m') = '2024-11'
GROUP BY 
    c.category_name;

-- Query for Month-over-Month Spending Trends by Category
SELECT 
    c.category_name, 
    DATE_FORMAT(t.transaction_date, '%Y-%m') AS month, 
    SUM(t.amount) AS total_spent
FROM 
    Transactions t
JOIN 
    Categories c ON t.category_id = c.category_id
GROUP BY 
    c.category_name, month
ORDER BY 
    month DESC;