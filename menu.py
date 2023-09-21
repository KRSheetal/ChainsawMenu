"""
A menu - you need to add the database and fill in the functions. 
"""

# create database table OR set up Peewee model to create table
import sqlite3


db_url = 'chainsaw_records.sqlite'

def create_table():
    with sqlite3.connect(db_url) as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS chainsaw_records (name text, country text, number_of_catches int)')
    conn.close()

def main():
    create_table() # create a table by calling the function

    menu_text = """
    1. Display all records
    2. Search by name
    3. Add new record
    4. Edit existing record
    5. Delete record 
    6. Quit
    """

    while True:
        print(menu_text)
        choice = input('Enter your choice: ')
        if choice == '1':
            display_all_records()
        elif choice == '2':
            search_by_name()
        elif choice == '3':
            add_new_record()
        elif choice == '4':
            edit_existing_record()
        elif choice == '5':
            delete_record()
        elif choice == '6':
            break
        else:
            print('Not a valid selection, please try again')

    
def display_all_records():
    # displays all records
    conn = sqlite3.connect(db_url)
    results = conn.execute('SELECT * FROM chainsaw_records')
    print('All records: ')
    for row in results:
        print(f'{row[0]} | {row[1]} | {row[2]}')
    
    conn.close()


def search_by_name():
    # display the name the user enters
    search_term = input('Enter the name you want to search: ')
    conn = sqlite3.connect(db_url)
    results = conn.execute('SELECT name, * FROM chainsaw_records WHERE UPPER(name) like UPPER(?)', (search_term, ))
    if results:
        print('Found the record: ')
        for row in results:
            print(f'{row[0]} | {row[1]} | {row[2]}') # prints in a table format
    else:
        print('Name not found')

    conn.close()
  #  print('todo ask user for a name, and print the matching record if found. What should the program do if the name is not found?')


def add_new_record():
    # add new name, country and count
    new_name = input('Enter the full name of the new record holder: ')
    new_country = input(f'Enter the country that {new_name} is from: ')
    new_count = int(input(f'Enter how many chainsaw catches {new_name} made as a numeral: '))
    add_sql = 'insert into chainsaw_records (name, country, number_of_catches) VALUES (?, ?, ?)'
    with sqlite3.connect(db_url) as conn:
        conn.execute(add_sql, (new_name, new_country, new_count))
    conn.close()

def edit_existing_record():
    # updates the table
    search_term = input('Enter the name of the record holder you want to update: ')
    conn = sqlite3.connect(db_url)
    results = conn.execute('SELECT * FROM chainsaw_records WHERE UPPER(name) like UPPER(?)', (search_term,))
    if results:
        row = results.fetchone()
        name = row[0]
        print('Is this the record you want to update? ')
        print(f'{row[0]} | {row[1]} | {row[2]}')

        new_country = input(f'Enter the new country that {name} is from: ')
        new_count = int(input(f'Enter how many chainsaw catches {name} made as a numeral: '))
        edit_sql = 'update chainsaw_records set country = ?, number_of_catches = ? where name = ?'
        with sqlite3.connect(db_url) as conn:
            conn.execute(edit_sql, (new_country, new_count, name))
    else:
        print('Name not found')
    
    conn.close()


def delete_record():
    # deletes the name the user entered 
    delete_term = input('Enter the name you want to delete: ')
    with sqlite3.connect(db_url) as conn:
        deleted = conn.execute('DELETE from chainsaw_records WHERE name = ?', (delete_term, ))
        delete_count = deleted.rowcount
    conn.close()

    # print confirmation message if deleted and if name not found.
    if delete_count == 0:
        print('Name not found!')
    else:
        print(f'{delete_term} is Deleted!')

if __name__ == '__main__':
    main()