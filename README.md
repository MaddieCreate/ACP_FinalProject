## ACP_FinalProject

# Smart Pricing Model

# I. Project Overview
  The Smart Pricing Model is designed to integrate your coffee shop's inventory, customers, and transactions into a simple centralized system to streamline operations. This application offers features such as time-based pricing adjustments, analysis of previous transactions, and login pages for administrative purposes, allowing users to add, edit, or delete menu items. This not only allows shop owners to modify their prices according to demand but also organizes the sales and customer records and inventory to a certain extent.

  The system fundamentally utilizes a MySQL database to manage important data such as customer details, transaction histories, and flexible pricing tables. Its design organizes key records into separate tables, including SmartPricing, Customers, Purchases, and TransactionHistory. This structure facilitates easy data access and updates, creating a robust backend to enhance a smooth user experience. The user interface is very engaging, featuring elements like login verification, a responsive menu, and forms tailored for specific actions such as adding or removing items. The dynamic pricing functionality is especially creative, as it modifies prices according to set time multipliers (morning, afternoon, evening), mirroring changes in real-world demand. This allows coffee shop owners to optimize profits during busy periods while efficiently managing their inventory. The Smart Pricing Model is a perfect fit for small to medium-sized coffee shops that want to embrace technology in their operations. Its dynamic pricing feature meets the needs of today’s consumers, and the database-driven design guarantees that it can grow with your business while remaining dependable. Plus, it’s easy to learn, allowing for a quick transition that boosts efficiency and gives store owners important insights into their day-to-day activities. 

  With features such as dynamic pricing, inventory management, and thorough record-keeping, this system makes everyday tasks easier while opening doors for growth. It helps you boost revenue during busy times, manage stock to cut down on waste, and gain insights into what your customers prefer. This system truly addresses the practical needs of entrepreneurs who are eager to improve their businesses. In the end, it’s a move towards creating a smarter and more sustainable future for small business owners, one cup of coffee at a time


# II. Explanation of how Python concepts, libraries, etc. were apllied
## 1. Libraries used:
**- tkinter:** This is Python's standard GUI (Graphical User Interface) library. In this code, it's used to create windows, buttons, labels, and other interactive elements.

**- PIL (Python Imaging Library):** Used for image handling, specifically to load and display the background image.

**- mysql.connector:** Enables connection and interaction with MySQL databases.

**- time:** Provides time-related functions, used here for event debouncing.

## 2. Object-Oriented Programming (OOP): The entire application is structured as a class **CoffeeShopPOS**. this demonstrates key OOP principles:
**-** The class has an __init__ method (constructor) that sets up the initial state.

**-** Methods like **login(), main_screen(), add_item()** are class methods that perform specific actions.

**- self** is used to refer to the instance of the class, allowing methods to access and modify object attributes.

## 3. Database Interaction:
**-** The **connect_to_db()** method establishes a connection to a mySQL database.

**-** **create_table** method dynamically creates database tables if they don't exist.

**-** Methods like** add_item(), update_item(),** and **delete_item()** interact with the database using SQL queries.

**-** Uses parameterized queries for safe database interactions.

## 4. Error Handling:
**-** Extensive use of **try/except** blocks to catch and handle potential errors.

**-** **messagebox** from tkinter is used to display user-friendly error and success messages.

## 5. GUI design Techniques:
**-** Dynamic widget creation and destruction using methods like **clear_content().**

**-** Use of frames and labels to organize UI elements.

**-** Implementing login system with predefined user credentials.

**-** Creating popup windows for different functionalities.

## 6. Event Handling:
**-** Button commands linked to specific methods **(command=self.validate_login).**

**-** Event binding for interactive elements like the item deletion listbox.

**-** Implementing debouncing in the delete item method to prevent rapid, unintended actions.

## 7. Data Manipulation:
**-** Dynamic price calculation based on time of day.

**-** Inventory and pricing management.

**-** Transaction and history tracking.

## 8.  Advance Python Features:
**-** List comprehensions.

**-** Dictionary usage for user authentication.

**-** Timestamp handling.

**-** Type conversion (string to float/int).

## 9. Main Function:
**- if __name__ == "__main__":** block ensures the application runs only when the script is directly executed.


# III. SDG and its integration into the project
## SDG 8: Decent Work and Economic Growth
  The system supports the growth of small and medium-sized businesses, like coffee shops, by optimizing pricing strategies and improving how they operate. With dynamic pricing, businesses can boost their revenue by adjusting to changes in customer demand. At the same time, effective inventory management helps minimize waste and avoid overstocking, making it easier for owners to run their shops smoothly.

## SDG 9: Industry, Innovation, and Infrastructure
  This project is a great example of how digital innovation can breathe new life into traditional business practices. By incorporating dynamic pricing algorithms, effective database management, and an easy-to-use interface, the system helps small businesses embrace modern technology and build a strong digital foundation

## SDG 12: Responsible Consumption and Production
  Inventory management and dynamic pricing play a key role in cutting down waste and encouraging responsible consumption. By matching inventory levels to actual demand, the system helps prevent overproduction and spoilage, making product management more sustainable.


# IV. Instruction for running the program
  1. Download the ZIP file containing the code.
  
  2. Unzip the file that includes:
  * Python code
  * SQL file containing database schema.
  * An asset folder with any necessary image.
  
  3. Open your mySQL then turn on both Apache and MySQL. Ensure both are running.
  
  4. Open phpMyadmin or click the admin next to MySQL and create database named spm_db.
  
  5. After creating, select it and import the included SQL file to set up the necessary tables.
 
  6. After that, go back to open the SmartPricingModel.py file and run the code using Python interpreter.
     
  7. Upon launching the program, a login screen will appear. Enter one of the predefined usernames(try maddie) and the corresponding password (maddie28) to access the system.
 
  8. Once you login, you can now perform the following action and explore the system.
