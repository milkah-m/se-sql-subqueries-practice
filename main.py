import sqlite3
import pandas as pd
conn = sqlite3.Connection('data.sqlite')

# 1. Write an Equivalent Query using a Subquery


q = """
SELECT 
customerNumber,
contactLastName,
contactFirstName
FROM customers
WHERE customerNumber IN(
SELECT customerNumber
FROM orders
WHERE orderDate = '2003-01-31'
)
"""
print("\n---Join to Subquery---\n")
print(pd.read_sql(q, conn))


# 2. Select the Total Number of Orders for Each Product Name

q = """
SELECT productName,
 COUNT(orderNumber) AS numberOrders,
 SUM(quantityOrdered) AS totalSold
FROM products
JOIN orderDetails
USING (productCode)
GROUP BY productName
ORDER BY totalSold DESC
"""

print("\n---Orders Total---\n")
print(pd.read_sql(q, conn))

# 3. Select the Product Name and the Total Number of People Who Have Ordered Each Product
# - Sort the results in descending order.

pd.read_sql(q, conn)
q = """
SELECT productName,
    (SELECT COUNT(DISTINCT customerNumber)
     FROM orders
     WHERE orderNumber IN (
         SELECT orderNumber
         FROM orderDetails
         WHERE orderDetails.productCode = products.productCode
     )
    ) AS totalPeople
FROM products
ORDER BY totalPeople DESC
"""

print("\n---Total Customers Per Product---\n")
print(pd.read_sql(q, conn))

# 4. Select the Employee Number, First Name, Last Name, City (of the office), and Office Code of the Employees who sold products
#  that have been ordered by fewer than 20 people.
# - Hint:  To start, think about how you might break the problem up. Be sure that your results only list each employee once.

q = """
SELECT DISTINCT employeeNumber, firstName, lastName, o.city, officeCode, quantityOrdered
FROM offices as o
JOIN employees as e
USING(officeCode)
JOIN customers as c
ON e.employeeNumber = c.salesRepEmployeeNumber
JOIN orders
USING(customerNumber)
JOIN orderDetails
USING(orderNumber)
WHERE productCode IN(SELECT productCode
FROM products
JOIN orderDetails
USING (productCode)
JOIN orders
USING (orderNumber)
GROUP BY productCode
HAVING(COUNT (DISTINCT customerNumber) < 20)
)
"""
print("\n---Less than 20--\n")
print(pd.read_sql(q, conn))

#  5. Select the Employee Number, First Name, Last Name, and Number of Customers for Employees whose customers have an average credit limit over 15K.

# q = """
# SELECT
#     employeeNumber,
#     firstName,
#     lastName,
#     COUNT(customerNumber) AS numCustomers
# FROM employees AS e
# JOIN customers As c
#     ON e.employeeNumber = c.salesRepEmployeeNumber
# GROUP BY employeeNumber
# HAVING AVG(creditLimit) > 15000
# ;
# """
pd.read_sql(q, conn)
q = """
SELECT employeeNumber, firstName, lastName, COUNT(customerNumber) as numberOfCustomers
FROM employees
JOIN customers
ON employees.employeeNumber = customers.salesRepEmployeeNumber
WHERE employeeNumber IN (
    SELECT salesRepEmployeeNumber
    FROM customers
    GROUP BY salesRepEmployeeNumber
    HAVING AVG(creditLimit) > 15000
)
GROUP BY employeeNumber, firstName, lastName
"""

print("\n---High Credit Limit--\n")
print(pd.read_sql(q, conn))