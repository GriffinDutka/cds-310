""" 
    Title: what_a_book.py
    Author: Griffin Dutka
    Date: 15 July 2022
    Description: WhatABook program
"""

""" import statements """
import sys
import mysql.connector
from mysql.connector import errorcode

""" database configuration object"""
config = {
    "user": "whatabook_user",
    "password": "MySQL8IsGreat!",
    "host": "127.0.0.1",
    "database": "whatabook",
    "raise_on_warnings": True
}

def show_menu():
    print("\n  --- Main Menu ---")

    print("    1. View Books\n    2. View Store Locations\n    3. My Account\n    4. Exit Program")

    try:
        choice = int(input('      <Example input: 1 for book listings>: '))

        return choice
    except ValueError:
        print("\n You entered an invalid number, program is being terminated...\n")

        sys.exit(0)

def show_books(_cursor):
    # The inner join query
    _cursor.execute("SELECT book_id, book_name, author, details from book")

    # obtain results from the cursor
    books = _cursor.fetchall()

    print("\n      --- DISPLAYING BOOK LISTINGS ---")

    # iterate player data set and display results
    for book in books:
        print("  Book Name: {}\n  Author: {}\n Details: {}\n".format(book[0], book[1], book[2]))

def show_locations(_cursor):
    _cursor.execute("SELECT store_id, locale from store")

    locations = _cursor.fetchall()

    print("\n      --- DISPLAYING STORE LOCATIONS ---")

    for location in locations:
        print("  Locale: {}\n".format(location[1]))

def validate_user():
    """ validate users ID """

    try:
        user_id = int(input('\n    Enter a customer ID <Example input: 1 for user_id 1>: '))

        if user_id < 0 or user_id > 3:
            print("\n  You entered an invalid customer number, program is being terminated...\n")
            sys.exit(0)

        return user_id
    except ValueError:
        print("\n You entered an invalid number, program is being terminated...\n")

        sys.exit(0)

def show_account_menu():
    """ display user account menu """

    try:
        print("\n      --- Customer Menu ---")
        print("        1. Wishlist\n        2. Add Book\n        3. Main Menu")
        account_option = int(input("        <Example input: 1 for wishlist>: "))

        return account_option
    except ValueError:
        print("\n  You entered an invalid number, program is being terminated...\n")

        sys.exit(0)

def show_wishlist(_cursor, _user_id):
    """ query database for list of books added to user wishlist """

    _cursor.execute("SELECT user.user_id, user.first_name, user.last_name, book.book_id, book.book_name, book.author " +
                    "FROM wishlist " +
                    "INNER JOIN user ON wishlist.user_id = user.user_id " +
                    "INNER JOIN book ON wishlist.book_id = book.book_id " +
                    "WHERE user.user_id = {}".format(_user_id))

    wishlist = _cursor.fetchall()

    print("\n      --- DISPLAYING WISHLIST ITEMS ---")

    for book in wishlist:
        print("        Book Name: {}\n        Author: {}\n".format(book[4], book[5]))

def show_books_to_add(_cursor, _user_id):
    """ query database for list of books not in user wishlist """
    
    query = ("SELECT book_id, book_name, author, details "
            "FROM book "
            "WHERE book_id NOT IN (SELECT book_id FROM wishlist WHERE user_id = {})".format(_user_id))

    print(query)

    _cursor.execute(query)

    books_to_add = _cursor.fetchall()

    print("\n     --- DISPLAYING AVAILABLE BOOKS ---")

    for book in books_to_add:
        print("        Book ID: {}\n        Book Name: {}\n".format(book[0], book[1]))

def add_book_to_wishlist(_cursor, _user_id, _book_id):
    _cursor.execute("INSERT INTO wishlist(user_id, book_id) VALUES({}, {}".format(_user_id, _book_id))

try:
    """ try/catch block for handling MYSQL db errors """

    db = mysql.connector.connect(**config) # connection to database

    cursor = db.cursor() # cursor for queries

    print("\n Welcome to the WhatABook Application! ")

    user_selection = show_menu() # display the main menu

    while user_selection != 4: # while the user selection is not 4

        if user_selection == 1: # if user selects 1, call show_books method and display the books
            show_books(cursor)

        if user_selection == 2: # if user selects 2, call the show_locations method and display locations
            show_locations(cursor)

# if the user selects 3, call the validate_user method to validate entered user_id then call the show_account_menu() to show the account settings menu
        if user_selection == 3: 
            my_user_id = validate_user()
            account_option = show_account_menu()

            while account_option != 3: # while account option does not equal 3

                if account_option == 1: # if the user selects 1, call show_wishlist() method to show current user configured wishlist items
                    show_wishlist(cursor, my_user_id)

                if account_option == 2: # if the user selects 2, call show_books_to_add function to show the user books not currently in the users' wishlist.

                    show_books_to_add(cursor, my_user_id) # show the books not currently configured in the users' wishlist

                    book_id = int(input("\n       Enter the ID of the book you want to add: "))

                    add_book_to_wishlist(cursor, my_user_id, book_id) # get the input book_id

                    db.commit() # commit changes to the database

                    print("\n      Book ID: {} was added to your wishlist!".format(book_id))

                if account_option < 0 or account_option > 3: # if the selected option is < 0 or > 3, display an invalid user selection 
                    print("\n     Invalid option, please try again. ")

                account_option = show_account_menu() # show the account menu

        if user_selection < 0 or user_selection > 4: # if the user selection is < 0 or > 4, display an invalid user selection
            print("\n     Invalid option, please try again. ")

        user_selection = show_menu() # show the main menu

    print("\n\n Program terminated...") # display program termination

except mysql.connector.Error as err:
    """ handle errors """

    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print( "  The supplied username or password are incorrect")
        
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("  The specified database doesn't exist")

    else:
        print(err)
    
finally:
    """ close connection to MySQL"""

db.close()