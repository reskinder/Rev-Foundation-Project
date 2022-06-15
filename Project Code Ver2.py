#
# Foundation Project (Version 2)
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
        passwd = userPasswd
    )

# CLOSE MYSQL CONNECTION FUNCTION
def CloseMySQL():
    # Disconnect from MySQL
    userdb.close()

# Welcome Prompt
print("Welcome to the Memory Library!")

# Connect to MySQL
ConnectMySQL()

# Disconnecting from MySQL