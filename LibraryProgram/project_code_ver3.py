#
# Foundation Project (Version 3)
# 06/15/22
# Project: Make a crude version of Goodreads w/ tables: ebook, physical, read, currently reading, want to read
#

# Imports
import mysql.connector                  # MySQL Connector Module
import maskpass                         # Used to mask password input
from tabulate import tabulate           # Used for printing MySQL tables in pretty format
from colorama import Fore, Back, Style  # Used for printing output with color (Fore: font color, Back: background color, Style: font style)
import csv                              # Used to read csv file with books (records) imported from Goodreads
import book_classes                     # Used to create new books (records) depending on shelf (table) type

# CONNECT TO MYSQL FUNCTION: Connects to MySQL server/workbench
def ConnectMySQL():
    # Check login info is valid
    while True:
        global userdb                   # Make connector variable global to be used anywhere in code
        # Check if login info works
        try:
            # Prompt user for login info for MySQL
            print("Enter the following login information for your MySQL Server:")
            loginHost = input("Host: ")
            userName = input("Username: ")
            userPasswd = maskpass.askpass(prompt="Password: ", mask="*")

            # Connect to MySQL w/ connector to create database
            userdb = mysql.connector.connect(
                host = loginHost,
                user = userName,
                passwd = userPasswd,
            )
        # Login info input does not work
        except:
            print("Login attempt failed. Either host, username, or password was incorrect.")
        # Login info worked, check if connection is successful
        else:
            # Connection successful
            if userdb.is_connected():
                print("Connection successful.\n")
                break
            # Connection unsuccessful
            else:
                print("Connection unsuccessful. Please try again.")

# CREATE SHELF (TABLE) FUNCTION: Permanent shelves cannot be deleted, custom shelves can
def CreateShelf(shelfType):
    # Create all permanent shelves: Ebook, Physical, Read (DoneReading), Currently Reading (CurrReading), & Want To Read (WantToRead)
    if shelfType == "P":
        # Ebook Shelf
        userCursor.execute("CREATE TABLE IF NOT EXISTS Ebook \
            (ASIN varchar(10) PRIMARY KEY, Title varchar(255), Series varchar(255), Author varchar(255), PublishDate varchar(8))")
        # Physical Shelf
        userCursor.execute("CREATE TABLE IF NOT EXISTS Physical \
            (ISBN varchar(13) PRIMARY KEY, Title varchar(255), Series varchar(255), Author varchar(255), PublishDate varchar(8))")
        # Read (DoneReading) Shelf
        userCursor.execute("CREATE TABLE IF NOT EXISTS DoneReading \
            (BookID varchar(13) PRIMARY KEY, FOREIGN KEY (BookID) REFERENCES Ebook(ASIN), FOREIGN KEY (BookID) REFERENCES Physical(ISBN), \
            Title varchar(255), Series varchar(255), Author varchar(255), PublishDate varchar(8), FinishDate varchar(8), Rating int, Review varchar(255))")
        # Currently Reading (CurrReading) Shelf
        userCursor.execute("CREATE TABLE IF NOT EXISTS CurrReading \
            (BookID varchar(13) PRIMARY KEY, FOREIGN KEY (BookID) REFERENCES Ebook(ASIN), FOREIGN KEY (BookID) REFERENCES Physical(ISBN), \
            Title varchar(255), Series varchar(255), Author varchar(255), PublishDate varchar(8), StartDate varchar(8))")
        # Want To Read (WantToRead) Shelf
        userCursor.execute("CREATE TABLE IF NOT EXISTS WantToRead \
            (BookID varchar(13) PRIMARY KEY, FOREIGN KEY (BookID) REFERENCES Ebook(ASIN), FOREIGN KEY (BookID) REFERENCES Physical(ISBN), \
            Title varchar(255), Series varchar(255), Author varchar(255), PublishDate varchar(8))")

    # Create custom shelf by user
    else:
        print("Custom Shelf Creation")

# MAIN LIBRARY MENU FUNCTION: Shows all shelves (tables), user selects which shelf to see & edit
def MainLibMenu():
    # Welcome Prompt
    print("Welcome to the Memory Library!")
    
    # Main Library Menu (while loop w/ True condition; break to end loop when needed)
    while True:
        # Select a shelf (menu choices 1 - 7)
        print("\nMemory Shelves:")
        print("1. Ebooks", "2. Physical Books", "3. Read", "4. Currently Reading", 
        "5. Want To Read", "6. Create Your Own Custom Shelf!", "7. Exit the Library", sep="\n")

        # Check user input is valid
        while True:
            # Check if user input is integer
            try:
                menuChoice = int(input("Select a shelf (1 - 7): "))
            # User input is not an integer
            except:
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
        if menuChoice == 1:         # Ebook Shelf
            userCursor.execute("SELECT * FROM Ebook")
            print(Fore.CYAN + "\nEBOOKS" + Style.RESET_ALL)
            print(tabulate(userCursor.fetchall(), headers=['ASIN', 'Title', 'Series', 'Author', 'Publish Date'], 
            tablefmt="fancy_grid", numalign="center", stralign="center"))

        elif menuChoice == 2:       # Physical Shelf
            userCursor.execute("SELECT * FROM Physical")
            print(Fore.CYAN + "\nPHYSICAL BOOKS" + Style.RESET_ALL)
            print(tabulate(userCursor.fetchall(), headers=['ISBN', 'Title', 'Series', 'Author', 'Publish Date'], 
            tablefmt="fancy_grid", numalign="center", stralign="center"))
        
        elif menuChoice == 3:       # Read Shelf
            userCursor.execute("SELECT * FROM DoneReading")
            print(Fore.CYAN + "\nREAD" + Style.RESET_ALL)
            print(tabulate(userCursor.fetchall(), headers=['BookID', 'Title', 'Series', 'Author', 'Publish Date', 'Finished Date', 'Rating', 'Review'], 
            tablefmt="fancy_grid", numalign="center", stralign="center"))
        
        elif menuChoice == 4:       # Currently Reading Shelf
            userCursor.execute("SELECT * FROM CurrReading")
            print(Fore.CYAN + "\nCURRENTLY READING" + Style.RESET_ALL)
            print(tabulate(userCursor.fetchall(), headers=['BookID', 'Title', 'Series', 'Author', 'Publish Date', 'Start Date'], 
            tablefmt="fancy_grid", numalign="center", stralign="center"))
        
        elif menuChoice == 5:       # Want To Read Shelf
            userCursor.execute("SELECT * FROM WantToRead")
            print(Fore.CYAN + "\nWANT TO READ" + Style.RESET_ALL)
            print(tabulate(userCursor.fetchall(), headers=['BookID', 'Title', 'Series', 'Author', 'Publish Date'], 
            tablefmt="fancy_grid", numalign="center", stralign="center"))
        
        elif menuChoice == 6:       # Custom Shelf Creation
            print("Custom Shelf Creation")
        
        elif menuChoice == 7:       # Exit Library (end program)
            print("Exiting the Memory Library. Have a nice day!")
            break

# SHELF MENU FUNCTION: Perform CRUD operations on selected shelf (Permanent shelves cannot be deleted, only the books in them can)
def ShelfEditMenu(shelfChoice):
    # Select an edit option (menu choices 1 - 5)
    print("\nShelf Options:")
    print("1. Add a book to shelf", "2. Search for a book", "3. Edit information of a book", 
    "4. Delete a book", "5. Delete shelf (custom shelves only)", "6. Return to list of shelves", sep="\n")

    # Check user input is valid
    while True:
        # Check if user input is integer
        try:
            menuChoice = int(input("Select a shelf option (1 - 5): "))
        # User input is not an integer
        except:
            print("Invalid input. You must enter a valid shelf option.")
        # Check if integer input was in range (1 - 5)
        else:
            # Input was in range
            if 1 <= menuChoice <= 5:
                break
            # Input was out of range
            else:
                print("Invalid input.", menuChoice, "is not a valid shelf option.")
    
    # Menu Choice Options
    if menuChoice == 1:
        print("Add a book (CREATE)")

        # Enter basic book information (bookID, Title, Series, Author, PublishDate)
        print("Enter the following information for your book:")
        newBook = book_classes.Book
        print("Enter the bookID (ASIN for Ebook, ISBN-13 for Physical)")
        newBook.bookID = input("BookID [E.g. ASIN (B0725PVK63), ISBN-13 (9781451656503)]: ")

        
    elif menuChoice == 2:
        print("Search for book (READ)")
    elif menuChoice == 3:
        print("Edit info of book (UPDATE)")
        # Execute statement for updating book info
        # userCursor.execute("UPDATE Physical SET ISBN = '9781451656503' WHERE (ISBN = '1451656505')")
    elif menuChoice == 4:
        print("Delete a book (DELETE)")
    elif menuChoice == 5:
        print("Delete custom shelf (DELETE)")
    else:
        print("Returning to list of shelves")

# Connect to MySQL & create cursor
ConnectMySQL()
userCursor = userdb.cursor()

# Create & use library (database)
userCursor.execute("CREATE DATABASE IF NOT EXISTS Memory")
userCursor.execute("USE Memory")

# Create all 5 permanent shelves (tables): Ebook, Physical, Read, Currently Reading, & Want To Read
CreateShelf("P")

# Main Library Menu
MainLibMenu()