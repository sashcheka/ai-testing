# Analyzing a Database Online

This project contains SQL queries to analyze sales data for an online store using SQLite.

## Setup Instructions

1. Go to [SQLite Online](https://sqliteonline.com/)
2. Copy and paste the following SQL script into the editor:

```sql
CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    customer TEXT,
    amount REAL,
    order_date DATE
);

INSERT INTO orders (customer, amount, order_date) VALUES
('Alice', 5000, '2024-03-01'),
('Bob', 8000, '2024-03-05'),
('Alice', 3000, '2024-03-15'),
('Charlie', 7000, '2024-02-20'),
('Alice', 10000, '2024-02-28'),
('Bob', 4000, '2024-02-10'),
('Charlie', 9000, '2024-03-22'),
('Alice', 2000, '2024-03-30');
```

3. Click "Run" to execute the script and create the table with sample data

## Tasks and Solutions

### Task 1: Calculate total sales volume for March 2024
```sql
SELECT SUM(amount) as total_sales
FROM orders
WHERE strftime('%Y-%m', order_date) = '2024-03';
```
Expected result: 27,000

### Task 2: Find the customer who spent the most overall
```sql
SELECT customer, SUM(amount) as total_spent
FROM orders
GROUP BY customer
ORDER BY total_spent DESC
LIMIT 1;
```
Expected result: Alice (20,000)

### Task 3: Calculate average order value for the last three months
```sql
SELECT AVG(amount) as average_order_value
FROM orders
WHERE order_date >= date('2024-01-01');
```
Expected result: 6,000

## Verification

After running each query, verify that your results match the expected values:
- Total sales for March: 27,000
- Top-spending customer: Alice (20,000)
- Average order value: 6,000

## Notes
- The queries use SQLite date functions like `strftime()` for date filtering
- The `GROUP BY` clause is used to aggregate data by customer
- The `ORDER BY` clause helps sort results in descending order
- The `LIMIT` clause restricts the output to the top result 