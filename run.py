import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint
from datetime import date


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('corner-shop')

"""
Welcome user and procees to User login, gets username from staff member.
"""
print("Welcome to The Sweet Spot Stock Control System")
username = input("Please enter your username: ")
print("Hello " + username)


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

        data_str = input("Enter your data here: ")

        sales_data = data_str.split(",")

        if validate_data(sales_data):
            print("Data is valid!")
            break

    return sales_data


def validate_data(values):
    """
    Inside the try, converts all string values into integers.
    Raises ValueError if strings cannot be converted into int,
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
    Update sales worksheet, add new row with the list data provided
    """
    print("Updating sales worksheet...\n")
    sales_worksheet = SHEET.worksheet("sales")
    sales_worksheet.append_row(data)
    print("Sales worksheet updated successfully.\n")

def update_stock_worksheet(data):
    """
    Update stock worksheet, add new row with the list data provided
    """
    print("Updating stock worksheet, please wait...\n")
    stock_worksheet = SHEET.worksheet("stock")
    stock_worksheet.append_row(data)
    print("Stock worksheet updated successfully.\n")

def calculate_remaining_data(sales_row):
    """
    Calculate remaining stock for each item by subtracting sales data from stock data
    """
    print("Calculating remaining stock, please wait...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]

    remaining_data = []
    for stock, sales in zip(stock_row, sales_row):
        remaining = int(stock) - sales
        remaining_data.append(remaining)
    
    return remaining_data

def check_and_order_stock(remaining_data):
    print("Checking if any items need reordering...\n")  
    order_worksheet = SHEET.worksheet("orders")
    orders_to_place = []

    for index, remaining in enumerate(remaining_data):
        if remaining < 10:
            item_name = f"Item {index+1}"
            order_quantity = 20
            order_date = date.today().strftime("%Y-%m-%d")
            orders_to_place.append([item_name, order_quantity, order_date])
        
    if orders_to_place:
        print("Placing orders for items with low stock....\n")
        for order in orders_to_place:
            order_worksheet.append_row(order)
            print("Orders placed successfully!\n")
    else:
            print("No items need reordering\n")

def main():
    """ 
    Run all program functions
    """
data = get_sales_data()
sales_data = [int(num) for num in data]
update_sales_worksheet(sales_data)
new_remaining_data = calculate_remaining_data(sales_data)
update_stock_worksheet(new_remaining_data)
check_and_order_stock(new_remaining_data)

main()