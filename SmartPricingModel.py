from tkinter import *
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector
import SPM_db     #database module
import time

class CoffeeShopPOS:
    def __init__(self, root):
        
#FOR WINDOW============================================================================================================
        self.root = root
        self.root.title("Smart Pricing Model")
        self.root.geometry("550x365")
        self.root.resizable(0, 0)
        
        # PREDEFINED LIST OF VALID USER (username: password)
        self.valid_users = {
            'maddie': 'maddie28', # admin
            'ivana': 'ivana22', # cashier
            'shane': 'shane14', # shift supervisor
            'kim': 'kim08', # marketing manager
            'johannes': 'johannes19' # sales representative
        }

        # INITIALIZED THE LOG IN SCREEM
        self.login()

#TO CLEAR ALL WIDGET=====================================================================================================
    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

#FUNCTION TO LOG IN=======================================================================================================
    def login(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        # ADD LOG IN LABELS AND FIELDS------------------------------------------------------------------------
        Label(self.root, text="Login", font=("Arial", 20)).pack(pady=20)

        Label(self.root, text="Username:").pack()
        self.username_entry = Entry(self.root)
        self.username_entry.pack(pady=5)

        Label(self.root, text="Password:").pack()
        self.password_entry = Entry(self.root, show="*")
        self.password_entry.pack(pady=5)

        Button(self.root, text="Login", command=self.validate_login).pack(pady=10)

    def validate_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username in self.valid_users and self.valid_users[username] == password:
            messagebox.showinfo("Login Success", "Welcome to the system!")
            self.main_screen()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

#FUNCTION FOR MAIN SCREEN======================================================================================================
    def main_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        #DATABASE CONNECTION----------------------------------------------------------------------------------------------
        self.con = self.connect_to_db()
        self.create_table()
          
        #ADDING BACKGROUND IMAGE----------------------------------------------------------------------------------------------
        self.bg_image = ImageTk.PhotoImage(Image.open("cafe.jpg"))
        self.bg_label = tk.Label(self.root, image=self.bg_image)
        self.bg_label.place(relwidth=1, relheight=1)  # Cover the entire content area  
        
        #FRAME FOR BUTT0NS---------------------------------------------------------------------------------------------------
        self.frame = tk.Frame(self.root, 
                              bg="#805E49",
                              width=220, 
                              height=430)
        self.frame.pack(side="right", 
                        fill="x", 
                        padx=10, 
                        pady=10, 
                        anchor='w')
        
        #FRAME FOR CONTENTS------------------------------------------------------------------------------------------------------- 
        self.content = tk.LabelFrame(self.root, 
                                     text="Smart Pricing Model", 
                                     fg="white", 
                                     bg="#805E49", 
                                     padx=10, 
                                     pady=10, 
                                     font=("Vivaldi", 20)
                                     )
        self.content.place(relwidth=0.6, relx=0.7, rely=0.1, anchor="ne", height=270)
        
        # BUTTONS FOR ACTION-------------------------------------------------------------------------------------------------------------
        tk.Button(self.frame, text="Settings", command=self.settings).pack(pady=12)
        tk.Button(self.frame, text="Add Item", command=self.add_item).pack(pady=12)
        tk.Button(self.frame, text="Update Item", command=self.update_item).pack(pady=12)
        tk.Button(self.frame, text="Delete Item", command=self.delete_item).pack(pady=12)
        tk.Button(self.frame, text="Get Dynamic Price", command=self.dynamic_price).pack(pady=12)
        tk.Button(self.frame, text="Show Menu", command=self.show_menu).pack(pady=12)
        tk.Button(self.frame, text="Exit", command=self.root.quit).pack(pady=12)

    def connect_to_db(self):
        return mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root", 
            password="", 
            database="SPM_db"
        )

# CREATE NECESSARY TABLES (Customers, Purchases, Sales, Transaction History)==============================================================
#CUSTOMERS TABLE--------------------------------------------------------------------------------------------------------------------
    def create_table(self):
        cur = self.con.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS Customers (
                customer_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                email VARCHAR(100)
            )
        """)
       
#PURCHASE TABLE-------------------------------------------------------------------------------------------------------------------- 
        cur.execute("""
            CREATE TABLE IF NOT EXISTS Purchases (
                purchase_id INT AUTO_INCREMENT PRIMARY KEY,
                customer_id INT,
                item_name VARCHAR(100),
                quantity INT,
                price FLOAT,
                purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
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
                sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
            )
        """)

#TRANSACTIONHISTORY TABLE--------------------------------------------------------------------------------------------------------------------   
        cur.execute("""
            CREATE TABLE IF NOT EXISTS TransactionHistory (
                transaction_id INT AUTO_INCREMENT PRIMARY KEY,
                customer_id INT,
                transaction_type ENUM('purchase', 'sale'),
                item_name VARCHAR(100),
                quantity INT,
                amount FLOAT,
                transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
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
        self.con.commit()
      
#SmartPricing TABLE--------------------------------------------------------------------------------------------------------------------  
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS SmartPricing (
                item_no INT AUTO_INCREMENT PRIMARY KEY,
                item_name VARCHAR(100) UNIQUE,
                base_price FLOAT,
                inventory INT,
                create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        self.con.commit()

#FUNCTION FOR SETTINGS -------------------------------------------------------------------------------------------------
    def settings(self):
        for widget in self.root.winfo_children():
             widget.destroy()

        # ADDING SETTINGS ABEL-------------------------------------------------------------------------------------------
        Label(self.root, text="Settings", font=("Arial", 20)).pack(pady=20)

        #BUTTON TO SHOW RECORD----------------------------------------------------------------------------------------------
        self.frame_buttons = tk.Frame(self.root)
        self.frame_buttons.pack(pady=10)

         #BUTTON FOR EACH CATEGORY---------------------------------------------------------------------------------------------
        tk.Button(self.frame_buttons, text="Customer Records", command=self.CustomerRec).pack(pady=5)
        tk.Button(self.frame_buttons, text="Purchase Records", command=self.PurchaseRec).pack(pady=5)
        tk.Button(self.frame_buttons, text="Sales Records", command=self.SalesRec).pack(pady=5)
        tk.Button(self.frame_buttons, text="Transaction Records", command=self.TransactionsRec).pack(pady=5)
        tk.Button(self.frame_buttons, text="View History", command=self.History).pack(pady=5)
       
        # BACK BUTTON TO RETURN-----------------------------------------------------------------------------------------------------
        Button(self.root, text="Back", command=self.main_screen).pack(pady=10)

#FUNCTION FOR CUSTOMERS' RECORD -----------------------------------------------------------------------------------------------------------
    def CustomerRec(self):
        customer_rec = tk.Toplevel(self.root)
        customer_rec.title("Customer Records")
        customer_rec.geometry("400x400")

        # ADDING CUSTOMERS' RECORD------------------------------------------------------------------------------------------------
        Label(customer_rec, text="Customer Records", font=("Arial", 16)).pack(pady=10)

        customer_data = [
            (1, "Jeno Lee", "Jeno@gmail.com"),
            (2, "Mark Lee", "Mark@gmail.com"),
            (3, "Jaehyun Jung", "Jae@gmail.com"),
            (4, "Andy Park", "Andy@gmail.com"),
            (5, "Jungwoo kim", "Jungwoo@gmail.com"),
            (6, "Hendery Huang", "Hendery@gmail.com"),
            (7, "Johnny Suh", "Johnny@gmail.com"),
            (8, "Jaemin Na", "Jaem@gmail.com"),
            (9, "Riku Maeda", "Riku@gmail.com"),
            (10, "Kun Qian", "Kun@gmail.com"),
        ]

        for customer in customer_data:
            Label(
                customer_rec,
                text=f"ID:  {customer[0]},    Name: {customer[1]},    Email: {customer[2]}",
                anchor="w",
            ).pack(pady=2, fill="x")
  
#FUNCTION FOR PURCHASE RECORD -------------------------------------------------------------------------------------------        
    def PurchaseRec(self):
        # Create a new window for purchase records
        purchase_rec = tk.Toplevel(self.root)
        purchase_rec.title("Purchase Records")
        purchase_rec.geometry("490x400")

        # ADDING PURCHASE RECORD------------------------------------------------------------------------------------------
        Label(purchase_rec, text="Purchase Records", font=("Arial", 16)).pack(pady=10)

        purchase_data = [
            (1, "Jeno Lee", "Hot Choco", 2, "2024-12-06"),
            (2, "Mark Lee", "Smoothies", 1, "2024-12-06"),
            (3, "Jaehyun Jung", "Croissant", 3, "2024-12-03"),
            (4, "Andy Park", "Sandwich", 2, "2024-12-01"),
            (5, "Jungwoo Kim", "Latte", 1, "2024-12-01"),
            (6, "Hendery Huang", "Cappuccino", 2, "2024-11-29"),
            (7, "Johnny Suh", "Tea", 1, "2024-11-29"),
            (8, "Jaemin Na", "Americano", 1, "2024-11-28"),
            (9, "Riku Maeda", "Cake", 3, "2024-11-13"),
            (10, "Kun Qian", "Bottled Drink", 2, "2024-11-11"),
        ]

        for purchase in purchase_data:
            Label(
                purchase_rec,
                text=f"ID:  {purchase[0]},     Customer: {purchase[1]},     Item: {purchase[2]}, "
                    f"    Quantity:  {purchase[3]},     Date:  {purchase[4]}",
                anchor="w",
            ).pack(pady=2, fill="x")
 
#FUNCTION FOR SALES RECORD -----------------------------------------------------------------------------------------------                 
    def SalesRec(self):
        sales_rec = tk.Toplevel(self.root)
        sales_rec.title("Sales Records")
        sales_rec.geometry("500x400")

        # ADDING SALES' RECORD--------------------------------------------------------------------------------------------
        Label(sales_rec, text="Sales Records", font=("Arial", 16)).pack(pady=10)

        sales_data = [
            (1, "Hot choco", 5, 2.5, "2024-12-06"),
            (2, "Smoothies", 3, 1.5, "2024-12-06"),
            (3, "Croissant", 6, 3.0, "2024-12-03"),
            (4, "Sandwich", 4, 4.0, "2024-12-01"),
            (5, "Latte", 2, 3.5, "2024-12-01"),
            (6, "Cappuccino", 5, 3.2, "2024-11-29"),
            (7, "Tea", 1, 2.5, "2024-11-29"),
            (8, "Americano", 2, 1.5, "2024-11-28"),
            (9, "Cake", 4, 3.0, "2024-11-13"),
            (10, "Bottled Drink", 3, 4.0, "2024-11-11"),
        ]

        for sale in sales_data:
            Label(
                sales_rec,
                text=f"ID:  {sale[0]},     Item: {sale[1]},     Quantity Sold:  {sale[2]}, "
                    f"    Price:  {sale[3]},     Date:  {sale[4]}",
                anchor="w",
            ).pack(pady=2, fill="x")
       
#FUNCTION FOR TRANSACTION RECORD ----------------------------------------------------------------------------------------- 
    def TransactionsRec(self):
        # Create a new window for transaction records
        transaction_rec = tk.Toplevel(self.root)
        transaction_rec.title("Transaction Records")
        transaction_rec.geometry("580x400")

        # ADDING TRANSACTION'S RCORD--------------------------------------------------------------------------------------
        Label(transaction_rec, text="Transaction Records", font=("Arial", 16)).pack(pady=10)

        transaction_data = [
            (1, "Jeno Lee", "Hot Choco", 5, 12.5, "2024-12-05"),
            (2, "Mark Lee", "Smoothies", 3, 4.5, "2024-12-04"),
            (3, "Jaehyun Jung", "Croissant", 6, 18.0, "2024-12-03"),
            (4, "Andy Park", "Sandwich", 4, 16.0, "2024-12-02"),
            (5, "Jungwoo Kim", "Latte", 2, 7.0, "2024-12-01"),
            (6, "Hendery Huang", "Cappuccino", 5, 16.0, "2024-11-30"),
            (7, "Johnny Suh", "Tea", 1, 2.5, "2024-11-29"),
            (8, "Jaemin Na", "Americano", 2, 3.0, "2024-11-28"),
            (9, "Riku Maeda", "Cake", 4, 12.0, "2024-11-27"),
            (10, "Kun Qian", "Bottled Drinks", 3, 12.0, "2024-11-26"),
        ]

        for transaction in transaction_data:
            Label(
                transaction_rec,
                text=f"ID:  {transaction[0]},     Customer: {transaction[1]},     Item: {transaction[2]}, "
                    f"    Quantity:  {transaction[3]},     Total:  {transaction[4]},     Date:  {transaction[5]}",
                anchor="w",
            ).pack(pady=2, fill="x")
         
#FUNCTION FOR GISTORY --------------------------------------------------------------------------------------------------     
    def History(self):
        history_rec = tk.Toplevel(self.root)
        history_rec.title("History")
        history_rec.geometry("500x400")

        Label(history_rec, text="Action History", font=("Arial", 16)).pack(pady=10)

        #TO FETCH HISTORY RECORD----------------------------------------------------------------------------------------------
        try:
            cur = self.con.cursor()
            cur.execute("SELECT action_type, item_name, timestamp FROM History ORDER BY timestamp DESC")
            rows = cur.fetchall()

            if not rows:
                Label(history_rec, text="No history available.", anchor="w").pack(pady=5)
            else:
                for row in rows:
                    action_label = f"{row[0]}: {row[1]} at {row[2]}"
                    Label(history_rec, text=action_label, anchor="w").pack(pady=2, fill="x")
        except Exception as e:
            messagebox.showerror("Error", f"Could not fetch history: {e}")
   
#**********************************************MAIN FUNCTIONS*******************************************************
#FUNCTION FOR ADDING AN ITEM ------------------------------------------------------------------
    def add_item(self):
        self.clear_content()

        tk.Label(self.content, text="Enter Item Name:").pack(pady=5)
        item_name_entry = tk.Entry(self.content, width=30)
        item_name_entry.pack(pady=5)

        tk.Label(self.content, text="Enter Base Price:").pack(pady=5)
        base_price_entry = tk.Entry(self.content, width=30)
        base_price_entry.pack(pady=5)

        tk.Label(self.content, text="Enter Inventory Level:").pack(pady=5)
        inventory_entry = tk.Entry(self.content, width=30)
        inventory_entry.pack(pady=5)

# FUNCTION TO SAVE YOUR CURRENTLY ADD ITEM ----------------------------------------------------
        def submit_item():
            item_name = item_name_entry.get()
            base_price = base_price_entry.get()
            inventory = inventory_entry.get()
            try:
                cur = self.con.cursor()
                cur.execute(
                    "INSERT INTO SmartPricing (item_name, base_price, inventory) VALUES (%s, %s, %s)",
                    (item_name, float(base_price), int(inventory)),
                )
                self.con.commit()
                
                cur.execute(
                    "INSERT INTO History (action_type, item_name) VALUES (%s, %s)",
                    ("Add Item", item_name)
                )
                self.con.commit()
                
                item_name_entry.delete(0, END)
                base_price_entry.delete(0, END)
                inventory_entry.delete(0, END)
                
                messagebox.showinfo("Success", f"Item '{item_name}' added!")
                
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(self.content, text="Add", command=submit_item).pack(pady=10)
    
# FUNCTION TO UPDATE THE ITEM IN THE DATABASE -----------------------------------------------
    def update_item(self):
        self.clear_content()

        try:
            cur = self.con.cursor()
            cur.execute("SELECT COUNT(*) FROM SmartPricing")
            count = cur.fetchone()[0]

            if count == 0:
                messagebox.showinfo("Info", "No items to update.")
                return

            tk.Label(self.content, text="Enter Item Name to Update:").pack(pady=5)
            item_name_entry = tk.Entry(self.content, width=30)
            item_name_entry.pack(pady=5)

            tk.Label(self.content, text="Enter New Base Price:").pack(pady=5)
            base_price_entry = tk.Entry(self.content, width=30)
            base_price_entry.pack(pady=5)

            tk.Label(self.content, text="Enter New Inventory Level:").pack(pady=5)
            inventory_entry = tk.Entry(self.content, width=30)
            inventory_entry.pack(pady=5)

# FUNCTION TO SHOW THE UPDATED ITEM ---------------------------------------------------------
            def submit_update():
                item_name = item_name_entry.get()
                new_price = base_price_entry.get()
                inventory = inventory_entry.get()
                try:
                    cur = self.con.cursor()
                    cur.execute(
                        "UPDATE SmartPricing SET base_price = %s WHERE item_name = %s",
                        (float(new_price), item_name),
                    )
                    
                    cur.execute(
                        "INSERT INTO History (action_type, item_name) VALUES (%s, %s)",
                        ("Update Item", item_name)
                    )

                    if cur.rowcount > 0:
                        self.con.commit()
                        item_name_entry.delete(0, END)
                        base_price_entry.delete(0, END)
                        inventory_entry.delete(0, END)
                        messagebox.showinfo("Success", f"Item '{item_name}' updated!")
                    else:
                        raise ValueError("Item not found.")
                except Exception as e:
                    messagebox.showerror("Error", str(e))

            tk.Button(self.content, text="Update", command=submit_update).pack(pady=10)

        except Exception as e:
            messagebox.showerror("Error", f"An error occured: {e}")
            
#FUNCTION TO DELETE THE ITEM -------------------------------------------------------------------
    def delete_item(self):
        """Show all items and allow deletion with immediate confirmation on click."""
        self.clear_content()

        try:
            cur = self.con.cursor()
            cur.execute("SELECT item_name FROM SmartPricing")
            items = cur.fetchall()

            if not items:
                messagebox.showinfo("Info", "No items available to delete.")
                return

            # CREATE LABEL FOR INSTRUCTION
            tk.Label(self.content, text="Select an Item to Delete:", font=("Arial", 12)).pack(pady=5)

            # CREATING LISTBOX
            item_listbox = tk.Listbox(self.content, width=30, height=10)
            item_listbox.pack(pady=5)

            # POPULATE THE LIST BOX WITH PRE-FETCH ITEM
            for item in items:
                item_listbox.insert(tk.END, item[0])

            last_event_time = {"time": 0}            
            
#TO SHOW THAT THE ITEM HAS BEEN DELETED --------------------------------------------------------
            def on_item_select(event):
                # Implement debouncing (0.3 seconds delay between events)
                current_time = time.time()
                if current_time - last_event_time["time"] < 0.3:
                    return
                last_event_time["time"] = current_time

                # Get the selected item
                selected_item = item_listbox.get(tk.ACTIVE)
                if not selected_item:
                    return

                # Ask for confirmation
                confirm = messagebox.askyesno(
                    "Confirm Deletion", f"Are you sure you want to delete '{selected_item}'?"
                )
                if confirm:
                    try:
                        # Perform deletion in the database
                        cur.execute("DELETE FROM SmartPricing WHERE item_name = %s", (selected_item,))
                        cur.execute(
                            "INSERT INTO History (action_type, item_name) VALUES (%s, %s)",
                            ("Delete Item", selected_item)
                        )
                        self.con.commit()
                        messagebox.showinfo("Success", f"Item '{selected_item}' deleted successfully!")

                        # Update the listbox after deletion
                        item_listbox.delete(tk.ACTIVE)
                    except Exception as e:
                        messagebox.showerror("Error", f"Could not delete item: {e}")

            # Bind the listbox to item selection with debouncing
            item_listbox.bind("<<ListboxSelect>>", on_item_select)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
    
#FUNCTION TO CALCULATE THE DYNAMIC PRICE --------------------------------------------------------
    def dynamic_price(self):
        self.clear_content()
        
        try:
            cur = self.con.cursor()
            cur.execute("SELECT COUNT(*) FROM SmartPricing")
            count = cur.fetchone()[0]

            if count == 0:
                messagebox.showinfo("Info", "currently no item.")
                return
            
            tk.Label(self.content, text="Enter Item Name:").pack(pady=5)
            item_name_entry = tk.Entry(self.content, width=30)
            item_name_entry.pack(pady=5)

            tk.Label(
                self.content, text="Enter Time of Day (morning/afternoon/evening):"
            ).pack(pady=5)
            time_of_day_entry = tk.Entry(self.content, width=30)
            time_of_day_entry.pack(pady=5)
        
#TO SHOW THE CALCULATED PRICE TOGETHER WITH CORRESPONDING ITEM -------------------------------------------
            def calculate_price():
                item_name = item_name_entry.get()
                time_of_day = time_of_day_entry.get().lower()
                time_multipliers = {"morning": 1.2, "afternoon": 1.0, "evening": 0.8}
                try:
                    cur = self.con.cursor()
                    cur.execute(
                        "SELECT base_price FROM SmartPricing WHERE item_name = %s",
                        (item_name,),
                    )
                    result = cur.fetchone()
                    if result and time_of_day in time_multipliers:
                        base_price = result[0]
                        dynamic_price = base_price * time_multipliers[time_of_day]
                        messagebox.showinfo(
                            "Dynamic Price",
                            f"The dynamic price for '{item_name}' is php{dynamic_price:.2f}.",
                        )
                    else:
                        raise ValueError("Item not found or invalid time of day.")
                except Exception as e:
                    messagebox.showerror("Error", str(e))

            tk.Button(self.content, text="Calculate", command=calculate_price).pack(pady=10)
        
        except Exception as e:
            messagebox.showerror("Error", f"An error occured: {e}")
        
#FUNCTION IN SHOWING THE MENU -------------------------------------------------------------------------
    def show_menu(self):
        self.clear_content()
        try:
            cur = self.con.cursor()
            cur.execute("SELECT item_name, base_price, inventory FROM SmartPricing")
            rows = cur.fetchall()
            if not rows:
                tk.Label(self.content, text="The menu is currently empty.").pack(pady=10)
            else:
                for row in rows:
                    tk.Label(
                        self.content,
                        text=f"{row[0]}: Base Price: php{row[1]:.2f}, Inventory: {row[2]}",
                    ).pack(pady=5)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            
# FOR RUNNING THE APPLICATION -----------------------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = CoffeeShopPOS(root)
    root.mainloop()