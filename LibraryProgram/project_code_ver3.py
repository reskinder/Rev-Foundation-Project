#
# Foundation Project (Version 3)
# 06/15/22
# Project: Make a crude version of Goodreads w/ tables: ebook, physical, read, currently reading, want to read
#

# Imports
from tracemalloc import start
import mysql.connector                  # MySQL Connector Module
import maskpass                         # Used to mask password input
from tabulate import tabulate           # Used for printing MySQL tables in pretty format
from colorama import Fore, Back, Style  # Used for printing output with color (Fore: font color, Back: background color, Style: font style)
import csv                              # Used to read csv file with books (records) imported from Goodreads

# CONNECT TO MYSQL FUNCTION: Connects to MySQL Server/Workbench
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
        except mysql.connector.Error:
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

# MAIN LIBRARY MENU FUNCTION: Shows all permanent shelves (tables), user selects which shelf to see & edit
def MainLibMenu():
    # Welcome Prompt
    print("Welcome to the Memory Library!")

    # Create all 5 permanent shelves (tables): Ebook, Physical, Read, Currently Reading, & Want To Read
    CreateShelf("P")

    # Main Library Menu (while loop w/ True condition; break to end loop when needed)
    while True:
        # Select a shelf (menu choices 1 - 7)
        print("\nMemory Shelves:")
        print("1. Ebooks", "2. Physical Books", "3. Read", "4. Currently Reading", 
        "5. Want To Read", "6. See Custom Shelves", "7. Exit the Library", sep="\n")

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
        if menuChoice == 1:             # Ebook Shelf
            # Display Shelf
            userCursor.execute("SELECT * FROM Ebook")
            print(Fore.CYAN + "\nEBOOKS" + Style.RESET_ALL)
            print(tabulate(userCursor.fetchall(), headers=['ASIN', 'Title', 'Series', 'Author', 'Publish Date'], 
            tablefmt="fancy_grid", numalign="center", stralign="center"))

            print("\nAll ebooks must go in either the Read, Currently Reading, or Want To Read shelf. \
                \nTo add, remove, or edit book information, select one of the three aforementioned shelves.")

        elif menuChoice == 2:           # Physical Shelf
            # Display shelf
            userCursor.execute("SELECT * FROM Physical")
            print(Fore.CYAN + "\nPHYSICAL BOOKS" + Style.RESET_ALL)
            print(tabulate(userCursor.fetchall(), headers=['ISBN', 'Title', 'Series', 'Author', 'Publish Date'], 
            tablefmt="fancy_grid", numalign="center", stralign="center"))

            print("\nAll physical books must go in either the Read, Currently Reading, or Want To Read shelf. \
                \nTo add, remove, or edit book information, select one of the three aforementioned shelves.")
        
        elif menuChoice == 3:           # Read Shelf
            # Display shelf
            userCursor.execute("SELECT * FROM DoneReading")
            print(Fore.CYAN + "\nREAD" + Style.RESET_ALL)
            print(tabulate(userCursor.fetchall(), headers=['BookID', 'Title', 'Series', 'Author', 'Publish Date', 'Finished Date', 'Rating', 'Review'], 
            tablefmt="fancy_grid", numalign="center", stralign="center"))

            # Go to Shelf Edit Menu
            ShelfEditMenu("DoneReading")
        
        elif menuChoice == 4:           # Currently Reading Shelf
            # Display Shelf
            userCursor.execute("SELECT * FROM CurrReading")
            print(Fore.CYAN + "\nCURRENTLY READING" + Style.RESET_ALL)
            print(tabulate(userCursor.fetchall(), headers=['BookID', 'Title', 'Series', 'Author', 'Publish Date', 'Start Date'], 
            tablefmt="fancy_grid", numalign="center", stralign="center"))

            # Go to Shelf Edit Menu
            ShelfEditMenu("CurrReading")
        
        elif menuChoice == 5:           # Want To Read Shelf
            # Display shelf
            userCursor.execute("SELECT * FROM WantToRead")
            print(Fore.CYAN + "\nWANT TO READ" + Style.RESET_ALL)
            print(tabulate(userCursor.fetchall(), headers=['BookID', 'Title', 'Series', 'Author', 'Publish Date'], 
            tablefmt="fancy_grid", numalign="center", stralign="center"))

            # Go to Shelf Edit Menu
            ShelfEditMenu("WantToRead")
        
        elif menuChoice == 6:           # Go to Custom Shelf Menu
            print("Go to Custom Shelf Menu")
        
        elif menuChoice == 7:           # Exit Library (end program)
            print("\nExiting the Memory Library. Have a nice day!")
            break

# CUSTOM SHELF MENU FUNCTION: Shows all custom shelves (tables), user selects which shelf to see & edit
def CustomShelfMenu():
    # Main Library Menu (while loop w/ True condition; break to end loop when needed)
    while True:
        # Select a shelf (menu choices 1 - 7)
        print("\nMemory Shelves:")
        print("1. Ebooks", "2. Physical Books", "3. Read", "4. Currently Reading", 
        "5. Want To Read", "6. See Custom Shelves", "7. Exit the Library", sep="\n")

# SHELF EDIT MENU FUNCTION: Perform CRUD operations on selected shelf (Permanent shelves cannot be deleted, only the books in them can)
def ShelfEditMenu(shelfChoice):
    # Select an edit option (menu choices 1 - 5)
    print("\nShelf Options:")
    print("1. Add a book to shelf", "2. Search for a book", "3. Edit information of a book", 
    "4. Delete a book", "5. Delete shelf (custom shelves only)", "6. Return to list of shelves", sep="\n")

    # Check user input is valid
    while True:
        # Check if user input is an integer
        try:
            menuChoice = int(input("Select a shelf option (1 - 5): "))
        # User input is not an integer
        except ValueError:
            print("Invalid input. You must enter a valid shelf option.")
        # Check if integer input is in range (1 - 5)
        else:
            # Input is in range
            if 1 <= menuChoice <= 5:
                break
            # Input is out of range
            else:
                print("Invalid input.", menuChoice, "is not a valid shelf option.")
    
    # Menu Choice Options
    if menuChoice == 1:                 # CREATE: Adding a new book (record)
        isEbook = True                  # Boolean for knowing if ebook (true) or physical (false)
        # Enter basic book information (BookID, Title, Series, Author, PublishDate)
        print("Enter the following information for your book:")

        # BookID
        while True:
            # Check for valid BookID
            bookID = input("BookID [e.g. ASIN for Ebook (B0725PVK63) or ISBN-13 for Physical (9781451656503)]: ")
            # ASIN & 10 characters
            if bookID.isalnum() and len(bookID) == 10:
                break
            # ISBN & 13 numbers
            elif bookID.isnumeric() and len(bookID) == 13:
                # First 3 numbers must be 978 or 979
                pre1 = "978"; pre2 = "979"
                validISBN = True
                for i in range(3):
                    # ISBN prefix matches 978 or 979
                    if bookID[i] == pre1[i] or bookID[i] == pre2[i]:
                        pass
                    # Invalid ISBN prefix
                    else:
                        validISBN = False
                        print("Invalid input. You must enter a valid ISBN-13.")
                if validISBN:
                    # Confirmed physical book
                    isEbook = False
                    break
            # Input was neither ASIN nor ISBN
            else:
                print("Invalid input. You must enter a valid bookID.")
        # Title
        title = input("Title: ")
        # Series
        series = input("Series (If the book is not in a series, just hit enter): ")
        # Author
        author = input("Author: ")
        # PublishDate
        while True:
            # Check for valid PublishDate
            publishDate = input("Publish Date (mm-dd-yy): ")
            # Valid date format
            if publishDate[0:2].isalnum() and publishDate[3:5].isalnum() and publishDate[6:8].isalnum() and publishDate[2:6:3] == "--":
                break
            # Invalid date format
            else:
                print("Invalid input. You must enter a valid date (e.g. 07-23-19).")
        
        # Add book to Ebook or Physical shelf
        if isEbook:                     # Ebook
            userCursor.execute("INSERT INTO Ebook VALUES ('%s', '%s', '%s', '%s', '%s')", (bookID, title, series, author, publishDate))
        else:                           # Physical
            userCursor.execute("INSERT INTO Physical VALUES ('%s', '%s', '%s', '%s', '%s')", (bookID, title, series, author, publishDate))

        # Enter specific book information specific to each shelf
        if shelfChoice == "DoneReading":    # Read Shelf
            # FinishDate
            finishDate = input("Finish Reading Date (mm-dd-yy): ")
            # Rating (1 - 5)
            while True:
                # Check if rating input is an integer
                try:
                    rating = int(input("Rating (1 - 5): "))
                # Rating input is not an integer
                except ValueError:
                    print("Invalid input. You must enter a valid rating.")
                # Check if integer input is in range (1 - 5)
                else:
                    # Input is in range
                    if 1 <= rating <= 5:
                        break
                    # Input is out of range
                    else:
                        print("Invalid input.", rating, "is not a valid rating.")
            # Review
            review = input("Review (If you don't want to leave a review, just hit enter): ")
            # Add to shelf
            userCursor.execute("INSERT INTO DoneReading VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')", (bookID, title, series, author, publishDate, finishDate, rating, review))
        elif shelfChoice == "CurrReading":  # Currently Reading Shelf
            # StartDate
            while True:
                # Check for valid StartDate
                startDate = input("Start Reading Date (mm-dd-yy): ")
                # Valid date format
                if startDate[0:2].isalnum() and startDate[3:5].isalnum() and startDate[6:8].isalnum() and startDate[2:6:3] == "--":
                    break
                # Invalid date format
                else:
                    print("Invalid input. You must enter a valid date (e.g. 07-23-19).")
            # Add to shelf
            userCursor.execute("INSERT INTO CurrReading VALUES ('%s', '%s', '%s', '%s', '%s', '%s')", (bookID, title, series, author, publishDate, startDate))
        else:                               # Want To Read Shelf
            # Add to shelf
            userCursor.execute("INSERT INTO WantToRead VALUES ('%s', '%s', '%s', '%s', '%s')", (bookID, title, series, author, publishDate))
        
    elif menuChoice == 2:               # READ: Search for a specific book(s) (record(s))
        print("Search for book (READ)")
    elif menuChoice == 3:               # UPDATE: Edit information of a book (record)
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

# Main Library Menu
MainLibMenu()

# Disconnect from MySQL Server
userdb.close()