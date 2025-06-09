# Import the libraries to connect to the database and present the information in tables
import sqlite3
from tabulate import tabulate

# This is the filename of the database to be used
DB_NAME = 'library_catalogue.db'

def print_query(view_name:str):
    ''' Prints the specified view from the database in a table '''
    print('')
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
    print(tabulate(results,headings))
    db.close()

# This is the SQL to connect to all the tables in the database
TABLES = (" borrowing "
           "LEFT JOIN person_info ON borrowing.library_card = person_info.library_card "
           "LEFT JOIN books ON borrowing.isbn = books.isbn "
           "LEFT JOIN genres ON books.genre_id = genres.genre_id ")

def print_parameter_query(fields:str, where:str, parameter):
    """ Prints the results for a parameter query in tabular form. """
    print('')
    db = sqlite3.connect(DB_NAME)
    cursor = db.cursor()
    sql = ("SELECT " + fields + " FROM " + TABLES + " WHERE " + where)
    cursor.execute(sql,(parameter,))
    results = cursor.fetchall()
    print(tabulate(results,fields.split(",")))
    db.close()  


menu_choice = ''
print('Welcome to the Library database\n')
while menu_choice != 'EXIT':
    menu_choice = input('Type the number for the information you want:\n'
                        '1: All info about the borrowings\n'
                        '2: All borrowings in alphabetical order\n'
                        '3: All books in alphabetical names\n'
                        '4: Everyone in the database in alphabetical order\n'
                        '5: Find all books published by a certain publisher\n'
                        '6: Find all books with a certain genre\n'
                        '7: All borrowins which are overdue\n'
                        '8: All borrowins which are nearly overdue\n'
                        'EXIT: To exit the menu\n\n'
                        'Type option here: ')
    menu_choice = menu_choice.upper()
    if menu_choice == '1':
        print_query('all_data')
    elif menu_choice == '2':
        print_query('alphabetical_borrowings')
    elif menu_choice == '3':
        print_query('alphabetical_books')
    elif menu_choice == '4':
        print_query('alphabetical_names')
    elif menu_choice == '5':
        publisher = input('\nWhich make publisher do you want to see: ')
        print_parameter_query("book_title, genre, author_surname, author_first_name, publisher, publication_date", "publisher = ? ORDER BY book_title",publisher)
    elif menu_choice == '6':
        genre = input('\nWhich make genre do you want to see: ').title()
        print_parameter_query("book_title, genre, author_surname, author_first_name, publisher, publication_date", "genre = ? ORDER BY book_title",genre)
    elif menu_choice == '7':
        print_query('overdue')
    elif menu_choice == '8':
        print_query('nearly_overdue')
    print('')