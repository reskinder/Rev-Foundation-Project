#
# Foundation Project (Version 3)
# 06/24/22
# Project: Make a crude version of Goodreads w/ tables: ebook, physical, read, currently reading, want to read
#

# Imports
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
            print(Fore.YELLOW + "Enter the following login information for your MySQL Server:" + Style.RESET_ALL)
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
                print(Fore.GREEN + "Connection successful." + Style.RESET_ALL)
                break
            # Connection unsuccessful
            else:
                print(Fore.RED + "Connection unsuccessful. Please try again." + Style.RESET_ALL)

# CREATE SHELF (TABLE) FUNCTION: Create the 5 shelves
def CreateShelves():
    # Ebook Shelf
    userCursor.execute("CREATE TABLE IF NOT EXISTS Ebook \
        (ASIN varchar(10) PRIMARY KEY, Title varchar(255), Series varchar(255), Author varchar(255), PublishDate varchar(8))")
    # Physical Shelf
    userCursor.execute("CREATE TABLE IF NOT EXISTS Physical \
        (ISBN varchar(13) PRIMARY KEY, Title varchar(255), Series varchar(255), Author varchar(255), PublishDate varchar(8))")
    # Read (DoneReading) Shelf
    userCursor.execute("CREATE TABLE IF NOT EXISTS DoneReading \
        (BookID varchar(13) PRIMARY KEY, Title varchar(255), Series varchar(255), Author varchar(255), PublishDate varchar(8), \
        FinishDate varchar(8), Rating int, Review varchar(255), EbookID varchar(10), FOREIGN KEY (EbookID) REFERENCES Ebook(ASIN), \
        PhysicalID varchar(13), FOREIGN KEY (PhysicalID) REFERENCES Physical(ISBN))")
    # Currently Reading (CurrReading) Shelf
    userCursor.execute("CREATE TABLE IF NOT EXISTS CurrReading \
        (BookID varchar(13) PRIMARY KEY, Title varchar(255), Series varchar(255), Author varchar(255), PublishDate varchar(8), \
        StartDate varchar(8), EbookID varchar(10), FOREIGN KEY (EbookID) REFERENCES Ebook(ASIN), PhysicalID varchar(13), \
        FOREIGN KEY (PhysicalID) REFERENCES Physical(ISBN))")
    # Want To Read (WantToRead) Shelf
    userCursor.execute("CREATE TABLE IF NOT EXISTS WantToRead \
        (BookID varchar(13) PRIMARY KEY, Title varchar(255), Series varchar(255), Author varchar(255), PublishDate varchar(8), \
        EbookID varchar(10), FOREIGN KEY (EbookID) REFERENCES Ebook(ASIN), PhysicalID varchar(13), \
        FOREIGN KEY (PhysicalID) REFERENCES Physical(ISBN))")

# MAIN LIBRARY MENU FUNCTION: Shows all shelves (tables), user selects which shelf to see & edit
def MainLibMenu():
    # Welcome Prompt
    print(Fore.BLUE + "\nWelcome to the Memory Library!" + Style.RESET_ALL)

    # Create all 5 shelves (tables): Ebook, Physical, Read, Currently Reading, & Want To Read
    CreateShelves()

    # Main Library Menu
    while True:
        # Select a shelf (menu choices 1 - 7)
        print(Fore.LIGHTMAGENTA_EX + "\nMemory Shelves:" + Style.RESET_ALL)
        print("1. Ebooks", "2. Physical Books", "3. Read", "4. Currently Reading", 
        "5. Want To Read", "6. Exit the Library", sep="\n")

        # Check user input is valid
        while True:
            # Check if user input is integer
            try:
                menuChoice = int(input("Select a shelf (1 - 6): "))
            # User input is not an integer
            except ValueError:
                print("Invalid input. You must enter a valid shelf number.")
            # Check if integer input was in range (1 - 6)
            else:
                # Input was in range
                if 1 <= menuChoice <= 6:
                    break
                # Input was out of range
                else:
                    print("Invalid input.", menuChoice, "is not a valid shelf number.")
        
        # Menu Choice Options
        if menuChoice == 1:             # Ebook Shelf
            # Display Shelf
            userCursor.execute("SELECT * FROM Ebook ORDER BY SUBSTRING(PublishDate, 5) DESC")
            print(Fore.CYAN + "\nEBOOKS" + Style.RESET_ALL)
            print(tabulate(userCursor.fetchall(), headers=['ASIN', 'Title', 'Series', 'Author', 'Publish Date'], 
            tablefmt="fancy_grid", numalign="center", stralign="center", maxcolwidths=[None, 25, 25, 25, None]))

            print("\nAll ebooks must go in either the Read, Currently Reading, or Want To Read shelf. \
                \nTo add, remove, or edit book information, select one of the three aforementioned shelves.")

        elif menuChoice == 2:           # Physical Shelf
            # Display shelf
            userCursor.execute("SELECT * FROM Physical ORDER BY SUBSTRING(PublishDate, 5) DESC")
            print(Fore.CYAN + "\nPHYSICAL BOOKS" + Style.RESET_ALL)
            print(tabulate(userCursor.fetchall(), headers=['ISBN', 'Title', 'Series', 'Author', 'Publish Date'], 
            tablefmt="fancy_grid", numalign="center", stralign="center", maxcolwidths=[None, 25, 25, 25, None]))

            print("\nAll physical books must go in either the Read, Currently Reading, or Want To Read shelf. \
                \nTo add, remove, or edit book information, select one of the three aforementioned shelves.")
        
        elif menuChoice == 3:           # Read Shelf
            # Display shelf
            userCursor.execute("SELECT BookID, Title, Series, Author, PublishDate, FinishDate, Rating, Review FROM DoneReading ORDER BY SUBSTRING(FinishDate, 5) DESC")
            print(Fore.CYAN + "\nREAD" + Style.RESET_ALL)
            print(tabulate(userCursor.fetchall(), headers=['BookID', 'Title', 'Series', 'Author', 'Publish Date', 'Finished Date', 'Rating', 'Review'], 
            tablefmt="fancy_grid", numalign="center", stralign="center", maxcolwidths=[None, 25, 25, 25, None, None, None, 45]))

            # Go to Shelf Edit Menu
            ShelfEditMenu("DoneReading")
        
        elif menuChoice == 4:           # Currently Reading Shelf
            # Display Shelf
            userCursor.execute("SELECT BookID, Title, Series, Author, PublishDate, StartDate FROM CurrReading ORDER BY SUBSTRING(StartDate)")
            print(Fore.CYAN + "\nCURRENTLY READING" + Style.RESET_ALL)
            print(tabulate(userCursor.fetchall(), headers=['BookID', 'Title', 'Series', 'Author', 'Publish Date', 'Start Date'], 
            tablefmt="fancy_grid", numalign="center", stralign="center", maxcolwidths=[None, 25, 25, 25, None, None]))

            # Go to Shelf Edit Menu
            ShelfEditMenu("CurrReading")
        
        elif menuChoice == 5:           # Want To Read Shelf
            # Display shelf
            userCursor.execute("SELECT BookID, Title, Series, Author, PublishDate FROM WantToRead ORDER BY SUBSTRING(PublishDate) DESC")
            print(Fore.CYAN + "\nWANT TO READ" + Style.RESET_ALL)
            print(tabulate(userCursor.fetchall(), headers=['BookID', 'Title', 'Series', 'Author', 'Publish Date'], 
            tablefmt="fancy_grid", numalign="center", stralign="center", maxcolwidths=[None, 25, 25, 25, None]))

            # Go to Shelf Edit Menu
            ShelfEditMenu("WantToRead")
        
        elif menuChoice == 6:           # Exit Library (end program)
            print(Fore.BLUE + "\nExiting the Memory Library. Have a nice day!" + Style.RESET_ALL)
            break

# SHELF EDIT MENU FUNCTION: Perform CRUD operations on selected shelf
def ShelfEditMenu(shelfChoice):
    # Shelf Edit Menu
    while True:
        # Select an edit option (menu choices 1 - 5)
        print(Fore.LIGHTMAGENTA_EX + "\nShelf Options:" + Style.RESET_ALL)
        print("1. Add a book to shelf", "2. Search for a book", "3. Edit information of a book", 
        "4. Delete a book", "5. Return to list of shelves", sep="\n")

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
        
        isEbook = True                  # Boolean for knowing if ebook (true) or physical (false)
        # Menu Choice Options
        if menuChoice == 1:                 # CREATE: Adding a new book (record)
            # Enter basic book information (BookID, Title, Series, Author, PublishDate)
            print("\nEnter the following information for your book:")

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
                userCursor.execute("INSERT INTO Ebook VALUES (%s, %s, %s, %s, %s)", (bookID, title, series, author, publishDate))
            else:                           # Physical Book
                userCursor.execute("INSERT INTO Physical VALUES (%s, %s, %s, %s, %s)", (bookID, title, series, author, publishDate))

            # Save changes made to database
            userdb.commit()
            
            # Enter specific book information specific to each shelf
            if shelfChoice == "DoneReading":    # Read Shelf
                # FinishDate
                while True:
                    # Check for valid FinishDate
                    finishDate = input("Finish Reading Date (mm-dd-yy): ")
                    # Valid date format
                    if finishDate[0:2].isalnum() and finishDate[3:5].isalnum() and finishDate[6:8].isalnum() and finishDate[2:6:3] == "--":
                        break
                    # Invalid date format
                    else:
                        print("Invalid input. You must enter a valid date (e.g. 07-23-19).")
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
                if isEbook:                 # Read Ebook
                    userCursor.execute("INSERT INTO DoneReading VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NULL)", (bookID, title, series, author, publishDate, finishDate, rating, review, bookID))
                    print("%s has been added to the Ebook Shelf and Read Shelf", title)
                else:                       # Read Physical Book
                    userCursor.execute("INSERT INTO DoneReading VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NULL, %s)", (bookID, title, series, author, publishDate, finishDate, rating, review, bookID))
                    print("%s has been added to the Physical Books Shelf and Read Shelf", title)
            
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
                if isEbook:                 # Currently Reading Ebook
                    userCursor.execute("INSERT INTO CurrReading VALUES (%s, %s, %s, %s, %s, %s, %s, NULL)", (bookID, title, series, author, publishDate, startDate, bookID))
                    print("%s has been added to the Ebook Shelf and Currently Reading Shelf", title)
                else:                       # Currently Reading Physical Book
                    userCursor.execute("INSERT INTO CurrReading VALUES (%s, %s, %s, %s, %s, %s, NULL, %s)", (bookID, title, series, author, publishDate, startDate, bookID))
                    print("%s has been added to the Physical Books Shelf and Currently Reading Shelf", title)
            
            else:                               # Want To Read Shelf
                # Add to shelf
                if isEbook:
                    userCursor.execute("INSERT INTO WantToRead VALUES (%s, %s, %s, %s, %s, %s, NULL)", (bookID, title, series, author, publishDate, bookID))
                    print("%s has been added to the Ebooks Shelf and Want To Read Shelf", title)
                else:
                    userCursor.execute("INSERT INTO WantToRead VALUES (%s, %s, %s, %s, %s, NULL, %s)", (bookID, title, series, author, publishDate, bookID))
                    print("%s has been added to the Physical Books Shelf and Want To Read Shelf", title)
            
            # Save changes made to database
            userdb.commit()
            print("Your book has been added.")
            
        elif menuChoice == 2:               # READ: Search for specific book(s) (record(s))
            # Search Book Options (1 - 5)
            print(Fore.LIGHTMAGENTA_EX + "\nSearch Options:" + Style.RESET_ALL)
            print("1. BookID", "2. Title", "3. Series", 
            "4. Author", "5. Publish Date", sep="\n")

            # Check user input is valid
            while True:
                # Check if user input is an integer
                try:
                    searchChoice = int(input("Select a search option (1 - 5): "))
                # User input is not an integer
                except ValueError:
                    print("Invalid input. You must enter a valid search option.")
                # Check if integer input is in range (1 - 5)
                else:
                    # Input is in range
                    if 1 <= searchChoice <= 5:
                        break
                    # Input is out of range
                    else:
                        print("Invalid input.", searchChoice, "is not a valid search option.")
            
            # Search Choice Options
            if searchChoice == 1:       # Search with BookID
                # Check user input is valid
                while True:
                    searchInput = input("Enter BookID (ASIN or ISBN-13): ")
                    # Valid bookID
                    if len(searchInput) == 10 or len(searchInput) == 13:
                        break
                    # Input was neither ASIN nor ISBN
                    else:
                        print("Invalid input. You must enter a valid bookID.")
                
                # Search & display results
                userCursor.execute("SELECT * FROM %s WHERE BookID = %s", (shelfChoice, searchInput))

            elif searchChoice == 2:     # Search with Title
                # User input
                searchInput = input("Enter Title: ")

                # Search & display results
                userCursor.execute(f"SELECT * FROM {shelfChoice} WHERE Title LIKE '%{searchInput}%' ")

            elif searchChoice == 3:     # Search with Series
                # User input
                searchInput = input("Enter Series: ")

                # Search & display results
                userCursor.execute(f"SELECT * FROM {shelfChoice} WHERE Series LIKE '%{searchInput}%' ")
            
            elif searchChoice == 4:     # Search with Author
                # User input
                searchInput = input("Enter Author: ")

                # Search & display results
                userCursor.execute(f"SELECT * FROM {shelfChoice} WHERE Author LIKE '%{searchInput}%' ")
            
            elif searchChoice == 5:     # Search with PublishDate
                # Check user input is valid
                while True:
                    searchInput = input("Publish Date (mm-dd-yy): ")
                    # Valid date format
                    if searchInput[0:2].isalnum() and searchInput[3:5].isalnum() and searchInput[6:8].isalnum() and searchInput[2:6:3] == "--":
                        break
                    # Invalid date format
                    else:
                        print("Invalid input. You must enter a valid date (e.g. 07-23-19).")
                
                # Search & display results
                userCursor.execute("SELECT * FROM %s WHERE PublishDate = %s", (shelfChoice, searchInput))

        elif menuChoice == 3:               # UPDATE: Edit information of a book (record)
            # Update Book Menu (1 - 5)
            print(Fore.LIGHTMAGENTA_EX + "\n Edit Options:" + Style.RESET_ALL)
            print("1. BookID", "1. Title", "3. Series", "4. Author", 
            "5. Publish Date", "6. Start Date", "7. Finished Date", "8. Rating", "9. Review", sep="\n")
            print(Fore.LIGHTYELLOW_EX + "NOTE: " + Style.RESET_ALL + 
            "Option 6 is for the Currently Reading Shelf only\n\tOptions 7 - 9 are for the Read Shelf only")

            # Check user input is valid
            while True:
                # Check if user input is an integer
                try:
                    editChoice = int(input("Which information are you editing? (1 - 9): "))
                # User input is not an integer
                except ValueError:
                    print("Invalid input. You must enter a valid edit option.")
                # Check if integer input is in range (1 - 9)
                else:
                    # Input is in range
                    if 1 <= editChoice <= 9:
                        break
                    # Input is out of range
                    else:
                        print("Invalid input.", editChoice, "is not a valid edit option.")

            # Check user input is valid for BookID
            while True:
                editCurr = input("Enter current BookID (ASIN or ISBN-13): ")
                # ASIN & 10 characters
                if editCurr.isalnum() and len(editCurr) == 10:
                    break
                # ISBN & 13 numbers
                elif editCurr.isnumeric() and len(editCurr) == 13:
                    # First 3 numbers must be 978 or 979
                    pre1 = "978"; pre2 = "979"
                    validISBN = True
                    for i in range(3):
                        # ISBN prefix matches 978 or 979
                        if editCurr[i] == pre1[i] or editCurr[i] == pre2[i]:
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
            
            # Search & display results
            userCursor.execute("SELECT * FROM %s WHERE BookID = %s", (shelfChoice, editChoice))

            # Edit Choice Options
            if editChoice == 1:             # Edit BookID
                # Check new BookID input
                while True:
                    bookID = input("Enter new BookID (ASIN or ISBN-13): ")
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
                
                # Edit book in shelves
                if isEbook:                 # Edit Ebook
                    userCursor.execute("UPDATE Ebook SET ASIN = %s WHERE (ASIN = %s)", (bookID, editCurr))
                else:                       # Edit Physical
                    userCursor.execute("UPDATE Physical SET ISBN = %s WHERE (ISBN = %s)", (bookID, editCurr))
                userCursor.execute("UPDATE %s SET BookID = %s WHERE (BookID = %s)", (shelfChoice, bookID, editCurr))
            
            elif editChoice == 2:           # Edit Title
                title = input("Enter new title: ")
                # Edit book in shelves
                if isEbook:                 # Edit Ebook
                    userCursor.execute("UPDATE Ebook SET Title = %s WHERE (ASIN = %s)", (title, editCurr))
                else:                       # Edit Physical
                    userCursor.execute("UPDATE Physical SET Title = %s WHERE (ISBN = %s)", (title, editCurr))
                userCursor.execute("UPDATE %s SET Title = %s WHERE (BookID = %s)", (shelfChoice, title, editCurr))
            
            elif editChoice == 3:           # Edit Series
                series = input("Enter new series (If the book is not in a series, just hit enter): ")
                # Edit book in shelves
                if isEbook:                 # Edit Ebook
                    userCursor.execute("UPDATE Ebook SET Series = %s WHERE (ASIN = %s)", (series, editCurr))
                else:                       # Edit Physical
                    userCursor.execute("UPDATE Physical SET Series = %s WHERE (ISBN = %s)", (series, editCurr))
                userCursor.execute("UPDATE %s SET Series = %s WHERE (BookID = %s)", (shelfChoice, series, editCurr))
            
            elif editChoice == 4:           # Edit Author
                author = input("Enter new author: ")
                # Edit book in shelves
                if isEbook:                 # Edit Ebook
                    userCursor.execute("UPDATE Ebook SET Author = %s WHERE (ASIN = %s)", (author, editCurr))
                else:                       # Edit Physical
                    userCursor.execute("UPDATE Physical SET Author = %s WHERE (ISBN = %s)", (author, editCurr))
                userCursor.execute("UPDATE %s SET Author = %s WHERE (BookID = %s)", (shelfChoice, author, editCurr))
            
            elif editChoice == 5:           # Edit PublishDate
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
                
                # Edit book in shelves
                if isEbook:                 # Edit Ebook
                    userCursor.execute("UPDATE Ebook SET PublishDate = %s WHERE (ASIN = %s)", (publishDate, editCurr))
                else:                       # Edit Physical
                    userCursor.execute("UPDATE Physical SET PublishDate = %s WHERE (ISBN = %s)", (publishDate, editCurr))
                userCursor.execute("UPDATE %s SET PublishDate = %s WHERE (BookID = %s)", (shelfChoice, publishDate, editCurr))
            
            elif editChoice == 6:           # Edit StartDate
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
                
                # Edit book in shelf
                userCursor.execute("UPDATE %s SET StartDate = %s WHERE (BookID = %s)", (shelfChoice, startDate, editCurr))
            
            elif editChoice == 7:           # Edit FinishDate
                # FinishDate
                while True:
                    # Check for valid FinishDate
                    finishDate = input("Finish Reading Date (mm-dd-yy): ")
                    # Valid date format
                    if finishDate[0:2].isalnum() and finishDate[3:5].isalnum() and finishDate[6:8].isalnum() and finishDate[2:6:3] == "--":
                        break
                    # Invalid date format
                    else:
                        print("Invalid input. You must enter a valid date (e.g. 07-23-19).")
                
                # Edit book in shelf
                userCursor.execute("UPDATE %s SET FinishDate = %s WHERE (BookID = %s)", (shelfChoice, finishDate, editCurr))
            
            elif editChoice == 8:           # Edit Rating
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
                
                # Edit book in shelf
                userCursor.execute("UPDATE %s SET Rating = %s WHERE (BookID = %s)", (shelfChoice, rating, editCurr))
            
            elif editChoice == 9:           # Edit Review
                # Review
                review = input("Review (If you don't want to leave a review, just hit enter): ")

                # Edit book in shelf
                userCursor.execute("UPDATE %s SET Review = %s WHERE (BookID = %s)", (shelfChoice, review, editCurr))

            # Save changes made to database
            userdb.commit()
            print("Your book has been edited.")
        
        elif menuChoice == 4:               # DELETE: Delete a book (record)
            # Check user input is valid for BookID
            while True:
                deleteInput = input("Enter BookID (ASIN or ISBN-13): ")
                # Valid bookID
                if len(deleteInput) == 10 or len(deleteInput) == 13:
                    break
                # Input was neither ASIN nor ISBN
                else:
                    print("Invalid input. You must enter a valid bookID.")
            
            # Delete book from shelf
            userCursor.execute("DELETE FROM %s WHERE BookID = %s", (shelfChoice, deleteInput))

            # Save changes made to database
            userdb.commit()
            print("Your book has been deleted.")
        
        elif menuChoice == 5:               # Return to Main Library Menu
            print("Returning to list of shelves")
            break

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