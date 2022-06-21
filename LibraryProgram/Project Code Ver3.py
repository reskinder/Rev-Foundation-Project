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

# CONNECT TO MYSQL FUNCTION
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

# # CREATE TABLE (SHELF) FUNCTION
# def createTable(tableName):


# Welcome Prompt
print("Welcome to the Memory Library!\n")

# Connect to MySQL & create cursor
ConnectMySQL()
userCursor = userdb.cursor()

# Create & use database (library)
userCursor.execute("CREATE DATABASE IF NOT EXISTS Memory")
userCursor.execute("USE Memory")

# # Create all permanent tables (shelves)
# createTable()

# Main Library Menu (use while loop w/ True condition & use break to end loop when needed)

## TEST RUN: Display table
userCursor.execute("DESCRIBE Ebook")
for column in userCursor.fetchall():
    print(column[0], end='\t')
print("")
userCursor.execute("SELECT * FROM Ebook")
for val in userCursor:
    print(*val, sep='\t')