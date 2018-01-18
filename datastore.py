
import os
from book import Book
import files as file
import json

DATA_DIR = 'data'
BOOKS_FILE_NAME = os.path.join(DATA_DIR, 'wishlist.txt')
COUNTER_FILE_NAME = os.path.join(DATA_DIR, 'counter.txt')

# separator = '^^^'  # a string probably not in any valid data relating to a book

book_list = []
counter = 0


def setup():
    """ Read book info from file, if file exists. """

    global counter

    # try:
    #     with open(BOOKS_FILE_NAME) as f:
    #         data = f.read()
    #         make_book_list(data)
    # except FileNotFoundError:
    #     # First time program has run. Assume no books.
    #     pass

    file.read(BOOKS_FILE_NAME, cb=make_book_list)

    try:
        # with open(COUNTER_FILE_NAME) as f:
        #     try:
        #         counter = int(f.read())
        #     except ValueError:
        #         counter = 0
        counter = file.read(COUNTER_FILE_NAME)
        if not counter:
            counter = 0
    except IOError:
        counter = len(book_list)


def shutdown():
    """Save all data to a file - one for books, one for the current counter value, for persistent storage"""

    output_data = make_output_data()

    # Create data directory
    # try:
    #     os.mkdir(DATA_DIR)
    # except FileExistsError:
    #     pass  # Ignore - if directory exists, don't need to do anything.

    file.write(DATA_DIR, BOOKS_FILE_NAME, output_data)
    file.write(DATA_DIR, COUNTER_FILE_NAME, counter)

    # with open(BOOKS_FILE_NAME, 'w') as f:
    #     f.write(output_data)
    #
    # with open(COUNTER_FILE_NAME, 'w') as f:
    #     f.write(str(counter))


def get_books(**kwargs):
    """ Return books from data store. With no arguments, returns everything. """

    global book_list

    if len(kwargs) == 0:
        return book_list

    if 'read' in kwargs:
        read_books = [book for book in book_list if book.read == kwargs['read']]
        return read_books


def add_book(book):
    """ Add to db, set id value, return Book"""

    global book_list

    book.id = generate_id()
    book_list.append(book)


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

        print(book.id)
        print(type(book.id))

        if book.id == book_id:
            book.read = True
            return True

    return False  # return False if book id is not found


def make_book_list(string_from_file):
    """ turn the string from the file into a list of Book objects"""

    global book_list

    if len(string_from_file) > 0 :
        book_json = json.loads(string_from_file)

        print(book_json)

        # books_str = string_from_file.split('\n')

        for json_obj in book_json:
            book = Book(json_obj["title"], json_obj["author"], bool(json_obj["read"]), int(json_obj["id"]))
            book_list.append(book)


# def make_output_data():
#     """ create a string containing all data on books, for writing to output file"""
#
#     global book_list
#
#     output_data = []
#
#     for book in book_list:
#         output = [book.title, book.author, str(book.read), str(book.id)]
#         output_str = separator.join(output)
#         output_data.append(output_str)
#
#     all_books_string = '\n'.join(output_data)
#
#     return all_books_string


# def make_output_data_test(b_list=None):
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

    all_books_string = ', '.join(output_data)

    return "[ " + all_books_string + " ]"

