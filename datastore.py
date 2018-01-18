import os
from book import Book
import files as file
import json
import valid

DATA_DIR = 'data'
BOOKS_FILE_NAME = os.path.join(DATA_DIR, 'wishlist.txt')
COUNTER_FILE_NAME = os.path.join(DATA_DIR, 'counter.txt')

book_list = []
counter = 0


def setup():
    """ Read book info from file, if file exists. """
    global counter

    # reads them BOOKS_FILE_NAME file and passes make_book_list() as a calllback
    file.read(BOOKS_FILE_NAME, cb=make_book_list)

    try:
        # reads COUNTER_FILE_NAME and loads it into memory
        counter = file.read(COUNTER_FILE_NAME)
        if not counter:
            counter = 0
    except IOError:
        counter = len(book_list)


def shutdown():
    """Save all data to a file - one for books, one for the current counter value, for persistent storage"""

    output_data = make_output_data()

    file.write(DATA_DIR, BOOKS_FILE_NAME, output_data)
    file.write(DATA_DIR, COUNTER_FILE_NAME, counter)


def get_books(**kwargs):
    """ Return books from data store. With no arguments, returns everything. """

    global book_list

    if len(kwargs) == 0:
        return book_list

    if 'read' in kwargs:
        if len(kwargs) == 1:
            read_books = [book for book in book_list if book.read == kwargs['read']]
            return read_books
        else:
            matching_books = [book for book in book_list if kwargs['string'] in book.title or kwargs['string'] in book.author]
            return matching_books
    else:
        if len(kwargs) == 1:
            matching_books = [book for book in book_list if kwargs['string'] in book.title or kwargs['string'] in book.author]
            return matching_books
        else:
            unread_books = [book for book in book_list if book.read != kwargs['read']]
            return unread_books


def get_book(book_id):
    """ gets individual book by id """
    global book_list

    for book in book_list:
        if valid.is_number(book_id):
            if book.id == int(book_id):
                return book
        else:
            if book_id in book.author or book_id in book_id.title:
                return book
    print("No book found with id {}.".format(book_id))


def update_book(updated_book):
    """ updates an individual book """
    global book_list

    for x in range(len(book_list)):
        if book_list[x - 1].id == updated_book.id:
            book_list.pop(x-1)
            book_list.append(updated_book)


def add_book(book):
    """ Add to db, set id value, return Book"""

    global book_list

    book.id = generate_id()
    book_list.append(book)

def delete_book(book):
    '''Delete book from db, and update'''

    global book_list

    book_list.remove(book)

    print("Book hella deleted!")


def generate_id():
    global counter
    counter += 1
    return counter


def set_read(book_id, read):
    """Update book with given book_id to read.
    Return True if book is found in DB and update
    is made, False otherwise."""

    global book_list

    for book in book_list:
        if book.id == book_id:
            book.read = True
            return True

    return False  # return False if book id is not found


def make_book_list(string_from_file):
    """ turn the string from the file into a list of Book objects"""

    global book_list

    if len(string_from_file) > 0:
        book_json = json.loads(string_from_file)

        for book in book_json:
            book_list.append(
                Book(
                    title=book["title"],
                    author=book["author"],
                    read=bool(book["read"]),
                    id=int(book["id"]),
                    stars=int(book["stars"]),
                    stars_str=book["stars_str"])
                )


def make_output_data(b_list=None):
    """ create a string containing all data on books, for writing to output file"""

    if not b_list:
        global book_list
        lst = book_list
    else:
        lst = b_list

    output_data = []

    for book in lst:
        output_str = book.getJSON()
        output_data.append(output_str)

    all_books_string = "[ " + ', '.join(output_data) + " ]"

    return all_books_string


