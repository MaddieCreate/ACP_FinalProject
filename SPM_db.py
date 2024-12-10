import mysql.connector

# Connect to MySQL Database
def connect():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="SPM_db"
    )

# Ensure the table exists
def create_table():
    con = connect()
    cur = con.cursor()
    
    cur.execute("""
            CREATE TABLE IF NOT EXISTS Customers (
                customer_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                email VARCHAR(100) UNIQUE NOT NULL,
            )
        """)
       
#PURCHASE TABLE-------------------------------------------------------------------------------------------------------------------- 
    cur.execute("""
            CREATE TABLE IF NOT EXISTS Purchases (
                purchase_id INT AUTO_INCREMENT PRIMARY KEY,
                customer_id INT,
                item_name VARCHAR(100),
                quantity INT,
                purchase_date DATE NOT NULL,
                FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
            )
        """)
    
#SALES TABLE--------------------------------------------------------------------------------------------------------------------    
    cur.execute("""
            CREATE TABLE IF NOT EXISTS Sales (
                sale_id INT AUTO_INCREMENT PRIMARY KEY,
                customer_id INT,
                item_name VARCHAR(100),
                quantity INT,
                sale_price FLOAT,
                sale_date DATE NOT NULL,
                FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
            )
        """)

#TRANSACTIONHISTORY TABLE--------------------------------------------------------------------------------------------------------------------   
    cur.execute("""
            CREATE TABLE IF NOT EXISTS TransactionHistory (
                transaction_id INT AUTO_INCREMENT PRIMARY KEY,
                customer_id INT,
                transaction_type ENUM('purchase', 'sale') NOT NULL,
                item_name VARCHAR(100) NOT NULL,
                quantity INT NOT NULL,
                amount FLOAT NOT NULL,
                transaction_date DATE NOT NULL,
                FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
            )
        """)
        
#HISTORY TABLE--------------------------------------------------------------------------------------------------------------------
    cur.execute("""
            CREATE TABLE IF NOT EXISTS History (
                history_id INT AUTO_INCREMENT PRIMARY KEY,
                action_type VARCHAR(50),
                item_name VARCHAR(100),
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

#SmartPricing TABLE--------------------------------------------------------------------------------------------------------------------
    cur.execute("""
        CREATE TABLE IF NOT EXISTS SmartPricing (
            id INT AUTO_INCREMENT PRIMARY KEY,
            item_name VARCHAR(100) UNIQUE,
            base_price FLOAT,
            inventory INT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    con.commit()
    con.close()

# Add an item to the database
def add_item(item_name, base_price, inventory):
    con = connect()
    cur = con.cursor()
    cur.execute(
        "INSERT INTO SmartPricing (item_name, base_price, inventory) VALUES (%s, %s, %s)",
        (item_name, base_price, inventory)
    )
    con.commit()
    con.close()

# View all items
def view_items():
    con = connect()
    cur = con.cursor()
    cur.execute("SELECT * FROM SmartPricing")
    rows = cur.fetchall()
    con.close()
    return rows

# Delete an item
def delete_item(item_name):
    con = connect()
    cur = con.cursor()
    cur.execute("DELETE FROM SmartPricing WHERE item_name = %s", (item_name,))
    con.commit()
    con.close()

# Update an item's price
def update_item_price(item_name, new_price):
    con = connect()
    cur = con.cursor()
    cur.execute(
        "UPDATE SmartPricing SET base_price = %s WHERE item_name = %s",
        (new_price, item_name)
    )
    con.commit()
    con.close()

# Search for an item by name
def search_item(item_name):
    con = connect()
    cur = con.cursor()
    cur.execute("SELECT * FROM SmartPricing WHERE item_name = %s", (item_name,))
    row = cur.fetchone()
    con.close()
    return row
