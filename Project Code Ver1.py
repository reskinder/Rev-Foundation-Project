#
# Foundation Project (Version 1)
# 06/14/22
# Project: Make a crude version of Goodreads w/ tables: ebook, physical, read, currently reading, want to read
# Note: All functions are written above the rest of the code
#

# Imports
import mysql.connector          # MySQL Connector Module
import maskpass                 # Used to mask password input
import csv                      # Used to read csv file with books imported from Goodreads

## WELCOME & INTRO FUNCTION
def IntroFunc():
    # Welcome Prompt
    print("Welcome to the Memory Library!")

    # Database Type Menu: prompt user to make choice on Library Database Type
    print("To begin creating your personal library, choose one of the following options:\n"
        "\t1. Create a library from scratch (manually insert book information)\n"
        "\t2. Create a library in a csv file with book information")
    
    # Menu While Loop
    while True:
        try:
            menuChoice = int(input("\nSelection: "))
        except:
            print("Invalid input. Please enter 1 or 2.\n")

        # Library Creation Instructions
        print("In order to create your personal library, you will need the following:\n"
            "1. ")

## CONNECT TO MYSQL FUNCTION
def ConnectMySQL():
    # Prompt user for password to MySQL Workbench
    userPasswd = maskpass.askpass(prompt="Enter your MySQL Workbench password: ", mask="*")

    # Connect to MySQL Workbench w/ connector to create database
    global userdb               # Make connector variable global to be used anywhere in code
    userdb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        passwd = userPasswd
    )

## CREATE & USE DATABASE FUNCTION
# def CreateDB():

## CLOSE CONNECTION FUNCTION