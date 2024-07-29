|      Test Category                      |      Description                                                                                                                      |      Expected Result                                                                                                |   |   |
|-----------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------|---|---|
|     Username and Password Validation    |                                                                                                                                       |                                                                                                                     |   |   |
|     Valid Username                      |     Enter a valid username (e.g., "Kelly").                                                                                           |     The system accepts the username and proceeds to the   password input stage.                                     |   |   |
|     Invalid Username                    |     Enter an invalid username (e.g., "Kelly123",   "Kelly_one").                                                                      |     The system rejects the username and prompts the user to   re-enter a valid username containing only letters.    |   |   |
|     Valid Password                      |     Enter a valid password (e.g., "123456").                                                                                          |     The system accepts the password and allows the user to   proceed to the next step.                              |   |   |
|     Invalid Password                    |     Enter an invalid password (e.g., "12345",   "abcdef", "12345a").                                                                  |     The system rejects the password and prompts the user to   re-enter a valid password of exactly 6 digits.        |   |   |
|     Sales Data Validation               |                                                                                                                                       |                                                                                                                     |   |   |
|     Correct Sales Data Format           |     Input correct sales data (e.g.,   "10,20,30,40,50,60").                                                                           |     The system accepts the sales data, validates it, and   proceeds to the next step.                               |   |   |
|     Incorrect Sales Data Format         |     Input incorrect sales data formats (e.g.,   "10,20,30", "abc,20,30,40,50,60",   "10;20;30;40;50;60").                             |     The system rejects the data and prompts the user to   re-enter the data in the correct format.                  |   |   |
|     Worksheet Updates                   |                                                                                                                                       |                                                                                                                     |   |   |
|     Sales Worksheet Update              |     Verify that the sales data is correctly appended to the   "sales" worksheet in Google Sheets.                                     |     The new sales data appears as a new row in the   "sales" worksheet.                                             |   |   |
|     Stock Levels Update                 |     Check that stock levels are updated based on the sales   data entered.                                                            |     The "stock" worksheet is updated with the new   remaining stock levels after subtracting the sales data.        |   |   |
|     Order Placement                     |     Confirm that orders are placed for items with stock levels   below the threshold (e.g., items with stock levels less than 10).    |     The "orders" worksheet is updated with the order   quantities for items needing reordering.                     |   |   |


Bugs Encountered and Resolutions

1. Bug: Username Validation Error
•	Description: The system accepted usernames with special characters and numbers, contrary to the requirement of only letters.
•	Steps Taken to Resolve:
1.	Reviewed the validate_username function to ensure it correctly uses the regex pattern "^[A-Za-z]+$".
2.	Verified that the regex pattern was implemented correctly in the code.
3.	Tested various usernames with numbers and special characters to confirm the issue was resolved.
•	Resolution: Updated the regex pattern and validated it to ensure that only usernames with letters are accepted.

2. Bug: Password Validation Acceptance
•	Description: The system accepted passwords with fewer or more than 6 digits, which should not be allowed.
•	Steps Taken to Resolve:
1.	Checked the validate_password function and its regex pattern r"^\d{6}$" to ensure it matches exactly 6 digits.
2.	Fixed any issues in the regex implementation.
3.	Tested various password lengths and formats to verify that only 6-digit passwords are accepted.
•	Resolution: Corrected the regex pattern and tested to confirm that the password validation is working as intended.

3. Invalid Input Handling for Yes/No Responses
•	Issue: The program did not handle inputs like "Y" or "N" correctly for continuing data entry.
•	Steps Taken to Resolve:
1.	Identified Problem: Limited handling of user responses for continuing data entry.
2.	Fix Applied: Updated input handling to check for variations in responses such as "y", "n", "yes", "no".
3.	Verification: Tested the input prompt to ensure it correctly processes all acceptable variations.



