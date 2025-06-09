# Import the libraries to connect to the database and present the information in tables
import sqlite3
from tabulate import tabulate

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
    print(tabulate(results,headings))
    db.close()

menu_choice = ''
print('Welcome to the Library database\n')
while menu_choice != 'EXIT':
    menu_choice = input('Type the number for the information you want:\n'
                        '1: All info about the borrowings\n'
                        '2: All borrowins in alphabetical order\n'
                        '3: All books in alphabetical names\n'
                        '4: Everyone in the database in alphabetical order\n'
                        '5: All books published by Bloomsbury\n'
                        '6: All books with the magic genre\n'
                        '7: All borrowins which are overdue\n'
                        '8: All borrowins which are nearly overdue\n'
                        'EXIT: To exit the menu\n\n'
                        'Type option here: ')
    menu_choice = menu_choice.upper()