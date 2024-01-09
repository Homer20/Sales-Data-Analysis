import sqlite3
import random
import datetime
import pandas as pd

# SQL commands for creating the tables
create_sales_table = '''CREATE TABLE IF NOT EXISTS sales (
                sale_id INTEGER PRIMARY KEY,
                sale_date DATE,
                customer_id INTEGER,
                product_id INTEGER,
                quantity INTEGER,
                unit_price DECIMAL(10,2),
                total_price DECIMAL(10,2),
                FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
                FOREIGN KEY (product_id) REFERENCES products(product_id)
                )'''
                 

create_products_table = '''CREATE TABLE IF NOT EXISTS products (
                    product_id INTEGER PRIMARY KEY,
                    product_name TEXT,
                    product_price DECIMAL(10,2)
                )'''


create_employees_table = '''CREATE TABLE IF NOT EXISTS customers (
                    customer_id INTEGER PRIMARY KEY,
                    first_name TEXT,
                    last_name TEXT,
                    email TEXT,
                    phone TEXT
                )'''


# SQL commands for inserting sample data into the tables
insert_products_data = '''INSERT INTO products (product_name, product_price) VALUES (?, ?)'''
insert_sales_data = '''INSERT INTO sales (sale_date, customer_id, product_id, quantity, unit_price, total_price) VALUES (?, ?, ?, ?, ?, ?)'''
insert_employees_data = '''INSERT INTO employees (first_name, last_name, email, phone) VALUES (?, ?, ?, ?)'''

# Sample data for the products and customers tables

product_excel_file = 'products_sold.xlsx'
product_df = pd.read_excel(product_excel_file)
products = list(product_df[['Product', 'Price ($)']].itertuples(index=False, name=None))
#print(products)

# employees = [
#     ('Micheal', 'Scott', 'mscott@gmail.com', '555-123-4567'),
#     ('Dwight', 'Schrute', 'beetfarms@gmail.com', '555-987-6543'),
#     ('Pam', 'Beesly', 'beeslypam23@gmail.com', '555-456-7890'),
#     ('Jim', 'Halpert', 'jimhalp@hotmail.com', '555-234-5678'),
#     ('Angela', 'Martin', 'amartin@gmail.com', '555-789-0123'),
#     ('Kevin', 'Malone', 'chiliman@gmail.com', '555-345-6789'),
#     ('Oscar', 'Martinez', 'omartinez@hotmail.com', '555-901-2345'),
#     ('Ryan', 'Howard', 'howard@gmail.com', '555-567-8901'),
#     ('Kelly', 'Kapoor', 'kelly@gmail.com', '555-678-9012'),
#     ('Toby', 'Flenderson', 'flends@yahoo.com', '555-789-0123')
# ]

employee_excel_file = 'employee_info.xlsx'

employee_df = pd.read_excel(employee_excel_file)

employees = list(employee_df[['First Name', 'Last Name', 'Email', 'Phone Number']].itertuples(index=False, name=None))

# Define start and end dates for generating sales data
start_date = datetime.date(2023, 1, 1)
end_date = datetime.date(2023, 12, 31)

# Connecting to the database and creating the tables
with sqlite3.connect('sales.db') as conn:
    conn.execute(create_sales_table)
    conn.execute(create_products_table)
    conn.execute(create_employees_table)

    # Inserting sample data into the products table
    for product in products:
        conn.execute(insert_products_data, product)
    
    # Inserting sample data into the customers table
    for employee in employees:
        conn.execute(insert_employees_data, employee)
    
    # Inserting sample data into the sales table
    for i in range(1000):
        sale_date = start_date + datetime.timedelta(days=random.randint(0, 364))
        customer_id = random.randint(1, len(employees))
        product_id = random.randint(1, len(products))
        quantity = random.randint(1, 10)
        unit_price = products[product_id - 1][1]
        total_price = quantity * unit_price
        conn.execute(insert_sales_data, (sale_date, customer_id, product_id, quantity, unit_price, total_price))
    
    # Committing the changes to the database
    conn.commit()

    print('Database created successfully!')