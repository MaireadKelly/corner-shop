import gspread
from google.oauth2.service_account import Credentials
import re
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
User login, gets username from staff member.
"""
username = input("Please enter your username: ")
print("Hello " + username)

def get_user_password():
    """ 
    Get users password to go forward to data input 
    """
    print("Password should be 6 digits long with NO spaces OR commas")
        
    data_int = input("Please enter your password: ")

get_user_password()


def get_sales_data():
    """ 
    Get sales data figures from user.
    Run a loop until a valid string of data is received from the user.
    Valid string is 6 numbers separated by commas.
    """
    print("Please enter sales data for today.")
    print("Data should be six numbers separated by commas")

    data_str = input("Please enter your data:\n")
    
    sales_data = data_str.split(",")
    print(sales_data)

get_sales_data()



  