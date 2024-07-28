import gspread
from google.oauth2.service_account import Credentials
from datetime import date
import re

# Define the scope of the API access
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

# Authorize and set up the Google Sheets client
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('corner-shop')

def validate_username(username):
    """
    Validate the username to ensure it contains only letters.
    """
    # Regex pattern to match only letters
    pattern = re.compile("^[A-Za-z]+$")
    # Return True if the username matches the pattern, otherwise False
    return bool(pattern.match(username))

def validate_password(password):
    """
    Validate the password to ensure it is exactly 6 digits.
    """
    # Regex pattern to match exactly 6 digits
    pattern = re.compile(r"^\d{6}$")
    # Return True if the password matches the pattern, otherwise False
    return bool(pattern.match(password))

# Welcome message and user login
print("Welcome to The Sweet Spot Stock Control System")

# Loop to repeatedly ask for username until valid
while True:
    username = input("Please enter your username: ")
    if validate_username(username):
        print("Hello " + username)
        break  # Exit loop if username is valid
    else:
        print("Invalid username. Please use letters only.")

# Loop to repeatedly ask for password until valid
while True:
    password = input("Please enter your 6-digit password: ")
    if validate_password(password):
        print("Password accepted.")
        break  # Exit loop if password is valid
    else:
        print("Invalid password. Please enter exactly 6 digits.")

def get_sales_data():
    """
    Get sales figures input from the user.
    Run a while loop to collect a valid string of data from the user
    via the terminal, which must be a string of 6 numbers separated
    by commas. The loop will repeatedly request data, until it is valid.
    """
    while True:
        print("Please enter sales data from the last market.")
        print("Data should be six numbers, separated by commas.")
        print("Example: 10,20,30,40,50,60\n")

        data_str = input("Enter your data here: \n")

        sales_data = data_str.split(",")

        if validate_data(sales_data):
            print("Data is valid!")
            break

    return sales_data

def validate_data(values):
    """
    Validate the sales data input by the user.
    Convert all string values into integers.
    Raise ValueError if strings cannot be converted into int,
    or if there aren't exactly 6 values.
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

    return True

def update_sales_worksheet(data):
    """
    Update the sales worksheet with the new sales data.
    Add a new row with the list of data provided.
    """
    print("Updating sales worksheet...\n")
    sales_worksheet = SHEET.worksheet("sales")
    sales_worksheet.append_row(data)
    print("Sales worksheet updated successfully.\n")

def update_stock_worksheet(data):
    """
    Update the stock worksheet with the new stock data.
    Add a new row with the list of data provided.
    """
    print("Updating stock worksheet, please wait...\n")
    stock_worksheet = SHEET.worksheet("stock")
    stock_worksheet.append_row(data)
    print("Stock worksheet updated successfully.\n")

def calculate_remaining_data(sales_row):
    """
    Calculate remaining stock for each item by subtracting sales data from the latest stock data.
    """
    print("Calculating remaining stock, please wait...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]
    item_names = stock[0]  # Get stock item names from the first row

    remaining_data = []
    for stock, sales in zip(stock_row, sales_row):
        try:
            remaining = int(stock) - sales
        except ValueError:
            print(f"Error: '{stock}' is not a valid number. Please check your stock data.")
            remaining = 0  # Default value in case of error
        remaining_data.append(remaining)
    
    return item_names, remaining_data

def check_and_order_stock(item_names, remaining_data, sales_data):
    """
    Check if any items need reordering and place orders if necessary.
    Use sales data to determine the order quantity.
    """
    print("Checking if any items need reordering...\n")
    orders_to_place = [0] * len(item_names)  # Initialize a list of zeros with the same length as item_names

    for index, (item, remaining, sales) in enumerate(zip(item_names, remaining_data, sales_data)):
        if remaining < 10:
            # Use sales total as order quantity
            orders_to_place[index] = sales  # Place order in the corresponding index
            print(f"{item} needs to be reordered")
            print(f"Order placed for {item}, quantity: {sales}")
    
    return orders_to_place

def update_orders_worksheet(orders):
    """
    Update the orders worksheet with the new order data.
    Add a new row with the list of order quantities.
    """
    print("Updating orders worksheet, please wait...\n")
    orders_worksheet = SHEET.worksheet("orders")
    orders_worksheet.append_row(orders)  # Append the list of order quantities

    print("Order check complete.\n")
    print("Orders worksheet updated successfully.\n")

def main():
    """
    Run all program functions in sequence, and ask the user if they want to input more sales data.
    """
    while True:  # Loop to allow repeated data entry
        data = get_sales_data()
        sales_data = [int(num) for num in data]
        update_sales_worksheet(sales_data)
        item_names, new_remaining_data = calculate_remaining_data(sales_data)
        update_stock_worksheet(new_remaining_data)
        orders = check_and_order_stock(item_names, new_remaining_data, sales_data)  # Pass sales_data to check_and_order_stock
        update_orders_worksheet(orders)  # Update orders worksheet with the generated orders

        # Ask the user if they want to input more sales data
        more_data = input("Would you like to input more sales data? (yes/no or y/n): ").strip().lower()
        if more_data not in ('yes', 'y'):
            print(f"Thank you {username}, all data successfully recorded.")
            break  # Exit the loop if the user does not want to input more data

# Run the main function to start the program
main()
