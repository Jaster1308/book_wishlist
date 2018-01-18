# Main program

import datetime
import ui, datastore
from book import Book


def handle_choice(choice):

    if choice == '1':
        show_unread()

    elif choice == '2':
        show_read()

    elif choice == '3':
        book_read()

    elif choice == '4':
        new_book()

    elif choice == '5':
        rate_book()

    elif choice == 'q':
        quit()

    else:
        ui.message('Please enter a valid selection')


def show_unread():
    """Fetch and show all unread books"""
    unread = datastore.get_books(read=False)
    ui.show_list(unread)


def show_read():
    """Fetch and show all read books"""
    read = datastore.get_books(read=True)
    ui.show_list(read)
    for x in read:
        today = datetime.date.today()
        print(today)

def book_read():
    """ Get choice from user, edit datastore, display success/error"""
    book_id = ui.ask_for_book_id()
    if datastore.set_read(book_id, True):
        ui.message('Successfully updated')
    else:
        ui.message('Book id not found in database')


def new_book():
    """Get info from user, add new book"""
    n_book = ui.get_new_book_info()
    datastore.add_book(n_book)
    ui.message('Book added: ' + str(n_book))


def rate_book():
    show_read()
    book_id = int(input("Which book would you like to rate? "))
    book = datastore.get_book(book_id)
    if book:
        set_stars(book)


def set_stars(book):
    stars = int(input("How many stars would you rate {}? (1 - 5) ".format(book.title)))
    book.stars = stars
    book.stars_str = star_string(stars)
    datastore.update_book(book)


def star_string(stars):
    stars_str = ""
    if stars >= 0:
        stars_str = "⭐️" * stars
    return stars_str


def quit():
    """Perform shutdown tasks"""
    datastore.shutdown()
    ui.message('Bye!')


def main():

    datastore.setup()

    quit = 'q'
    choice = None

    while choice != quit:
        choice = ui.display_menu_get_choice()
        handle_choice(choice)


if __name__ == '__main__':
    main()
