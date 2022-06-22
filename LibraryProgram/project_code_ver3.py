#
# Foundation Project (Version 3)
# 06/15/22
# Project: Make a crude version of Goodreads w/ tables: ebook, physical, read, currently reading, want to read
# Note: All functions are written above the rest of the code
#

# Imports
import mysql.connector          # MySQL Connector Module
import maskpass                 # Used to mask password input
import csv                      # Used to read csv file with books imported from Goodreads
from tabulate import tabulate   # Used for printing MySQL tables in pretty format

# CONNECT TO MYSQL FUNCTION: Connects to MySQL server/workbench
def ConnectMySQL():
    # Prompt user for login info for MySQL
    print("Enter the following login information for your MySQL Server:")
    loginHost = input("Enter the host for your MySQL Server: ")
    userName = input("Enter your MySQL Server username: ")
    userPasswd = maskpass.askpass(prompt="Enter your MySQL Server password: ", mask="*")

    # Connect to MySQL w/ connector to create database
    global userdb               # Make connector variable global to be used anywhere in code
    userdb = mysql.connector.connect(
        host = loginHost,
        user = userName,
        passwd = userPasswd,
    )

# CREATE PERMANENT SHELVES (TABLE) FUNCTION: Permanent shelves must exist, cannot be deleted
def CreatePermShelves():
    # Create all permanent shelves (tables): Ebook, Physical, Read (DoneRead), Currently Reading (CurrReading), & Want To Read (ToRead)
    userCursor.execute("CREATE TABLE IF NOT EXISTS Ebook \
        (ASIN varchar(255) PRIMARY KEY, Title varchar(255), Series varchar(255), Author varchar(255), PublishDate varchar(255))")
    userCursor.execute("CREATE TABLE IF NOT EXISTS Physical \
        (ISBN int PRIMARY KEY, Title varchar(255), Series varchar(255), Author varchar(255), PublishDate varchar(255))")
    userCursor.execute("CREATE TABLE IF NOT EXISTS DoneRead \
        (BookID varchar(255), FOREIGN KEY (BookID) REFERENCES Ebook(ASIN), FOREIGN KEY (BookID) REFERENCES Physical(ISBN), \
        Title varchar(255), Series varchar(255), Author varchar(255), PublishDate varchar(255))")
    userCursor.execute("CREATE TABLE IF NOT EXISTS CurrReading \
        (BookID varchar(255), FOREIGN KEY (BookID) REFERENCES Ebook(ASIN), FOREIGN KEY (BookID) REFERENCES Physical(ISBN), \
        Title varchar(255), Series varchar(255), Author varchar(255), PublishDate varchar(255), StartDate varchar(255))")
    userCursor.execute("CREATE TABLE IF NOT EXISTS ToRead \
        (BookID varchar(255), FOREIGN KEY (BookID) REFERENCES Ebook(ASIN), FOREIGN KEY (BookID) REFERENCES Physical(ISBN), \
        Title varchar(255), Series varchar(255), Author varchar(255), PublishDate varchar(255))")

# MAIN LIBRARY MENU FUNCTION: Shows all shelves (tables), user selects which shelf to see & do CRUD operations on
def MainLibMenu():
    # Main Library Menu (while loop w/ True condition; break to end loop when needed)
    while True:
        # Select a shelf menu (menu choices 1 - 7)
        print("1. Ebooks", "2. Physical", "3. Read", "4. Currently Reading", 
        "5. Want To Read", "6. Create Your Own Custom Shelf!", "7. Exit the Library", sep="\n")

        # Check user input is valid
        while True:
            # Check if user input is integer
            try:
                menuChoice = int(input("Select a shelf (1 - 7): "))
            # User input is not an integer
            except ValueError:
                print("Invalid input. You must enter a valid shelf number.")
            # Check if integer input was in range (1 - 7)
            else:
                # Input was in range
                if 1 <= menuChoice <= 7:
                    break
                # Input was out of range
                else:
                    print("Invalid input.", menuChoice, "is not a valid shelf number.")
        
        # Menu Choice Options
        if menuChoice == 1:
            print("Ebook Shelf")
        elif menuChoice == 2:
            print("Physical Shelf")
        elif menuChoice == 3:
            print("Read Shelf")
        elif menuChoice == 4:
            print("Currently Reading Shelf")
        elif menuChoice == 5:
            print("Want To Read Shelf")
        elif menuChoice == 6:
            print("Custom Shelf Creation")
        elif menuChoice == 7:
            print("Hope to see you again at the Memory Library!")
            break

# Connect to MySQL & create cursor
ConnectMySQL()
userCursor = userdb.cursor()

# Create & use library (database)
userCursor.execute("CREATE DATABASE IF NOT EXISTS Memory")
userCursor.execute("USE Memory")

# Create all 5 permanent shelves (tables): Ebook, Physical, Read, Currently Reading, & Want To Read
CreatePermShelves()

# Welcome Prompt
print("Welcome to the Memory Library!\n")

# Main Library Menu

## TEST RUN: Display Ebook & Physical tables
userCursor.execute("SELECT * FROM Ebook")
myresult = userCursor.fetchall()
print(tabulate(myresult, headers=['ASIN', 'Title', 'Series', 'Author', 'Publish Date'], tablefmt="fancy_grid"))

userCursor.execute("SELECT * FROM Physical")
myresult = userCursor.fetchall()
print(tabulate(myresult, headers=['ISBN', 'Title', 'Series', 'Author', 'Publish Date'], tablefmt="fancy_grid"))