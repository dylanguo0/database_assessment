# Import the libraries to connect to the database and present the information in tables
import sqlite3
from tabulate import tabulate
from easygui import *

# This is the filename of the database to be used
DB_NAME = 'library_catalogue.db'

def print_query(view_name:str):
    ''' Prints the specified view from the database in a table '''
    # Set up the connection to the database
    db = sqlite3.connect(DB_NAME)
    cursor = db.cursor()
    # Get the results from the view
    sql = "SELECT * FROM '" + view_name + "'"
    cursor.execute(sql)
    results = cursor.fetchall()
    # Get the field names to use as headings
    field_names = "SELECT name from pragma_table_info('" + view_name + "') AS tblInfo"
    cursor.execute(field_names)
    headings = list(sum(cursor.fetchall(),()))
    # Print the results in a table with the headings
    codebox("Here are the results:", "Results", tabulate(results,headings))
    db.close()

# This is the SQL to connect to all the tables in the database
BORROWING_TABLES = (" borrowing "
           "LEFT JOIN person_info ON borrowing.library_card = person_info.library_card "
           "LEFT JOIN books ON borrowing.isbn = books.isbn "
           "LEFT JOIN genres ON books.genre_id = genres.genre_id ")

BOOKS_TABLES = (" books "
            "LEFT JOIN genres ON books.genre_id = genres.genre_id ")

def print_parameter_query(fields:str, where:str, parameter):
    """ Prints the results for a parameter query in tabular form. """
    db = sqlite3.connect(DB_NAME)
    cursor = db.cursor()
    sql = ("SELECT " + fields + " FROM " + table + " WHERE " + where)
    cursor.execute(sql,(parameter,))
    results = cursor.fetchall()
    codebox("Here are the results:", "Results", tabulate(results,fields.split(",")))
    db.close()

while True:
    msg ="Please choose a query"
    title = "Welcome to the Library database"
    choices = ["All info about the borrowings", 
               "All borrowings order by surname", 
               "All books order by book name", 
               "Every borrower ordered by surname",
               "Find all books by a certain publisher",
               "Find all books with a certain genre",
               "All borrowings which are overdue",
               "All borrowings which are nearly overdue",
               "Number of borrowed and overdue books each person has",
               "Find a certain book"]
    choice = choicebox(msg, title, choices)
    if choice == 'All info about the borrowings':
        print_query('all_data')
    elif choice == 'All borrowings order by surname':
        print_query('alphabetical_borrowings')
    elif choice == 'All books order by book name':
        print_query('alphabetical_books')
    elif choice == 'Every borrower ordered by surname':
        print_query('alphabetical_names')
    elif choice == 'Find all books by a certain publisher':
        msg = "Which publisher do you want to see?"
        title = "Pick a publisher"
        choices = ["Bloomsbury",
                   "David Bateman Ltd",
                   "Hardie Grant Children's Publishing",
                   "Hyperion",
                   "Murdoch Books",
                   "Penguin Books",
                   "Penguin Random House",
                   "St. Martin's Griffin",
                   "Ten Speed Press",
                   "Usborne Publishing Ltd"]
        publisher = choicebox(msg, title, choices)
        table = BOOKS_TABLES
        print_parameter_query("book_title, genre, author_surname, author_first_name, publisher, publication_date", "publisher = ? ORDER BY book_title",publisher)
    elif choice == 'Find all books with a certain genre':
        msg = "Which genre do you want to see?"
        title = "Pick a genre"
        choices = ["Cooking",
                  "Fantasy",
                  "Magic",
                  "Monsters",
                  "Nonfiction",
                  "NZ Fiction"]
        genre = choicebox(msg, title, choices)
        table = BOOKS_TABLES
        print_parameter_query("book_title, genre, author_surname, author_first_name, publisher, publication_date", "genre = ? ORDER BY book_title",genre)
    elif choice == 'All borrowings which are overdue':
        print_query('overdue')
    elif choice == 'All borrowings which are nearly overdue':
        print_query('nearly_overdue')
    elif choice == 'Number of borrowed and overdue books each person has':
        print_query('number_borrowed')
    elif choice == 'Find a certain book':
        msg = "Type in the name of a book"
        title = "Find a certain book"
        book = enterbox(msg, title)
        table = BOOKS_TABLES
        print_parameter_query("book_title, genre, author_surname, author_first_name, publisher, publication_date", "book_title = ? ORDER BY book_title",book)
    else:
        break