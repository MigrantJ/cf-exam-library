# coding=utf-8


class Library(object):
    def __init__(self, name):
        self.name = name
        self._shelves = {}

    def __str__(self):
        return "{}".format(self.name)

    def add_shelves(self, *args):
        """Add shelf instances to the library. Can also accept
        non-Shelf objects, which will be stringified into a new shelf's name.
        """
        for shelf in args:
            try:
                shelf_key = shelf.name
                shelf_to_add = shelf
            except AttributeError:
                # init new shelf based on passed-in string
                shelf_key = str(shelf)
                shelf_to_add = Shelf(shelf_key)

            if shelf_key not in self._shelves:
                self._shelves[shelf_key] = shelf_to_add
            else:
                print("Cannot add '{shelf}': shelf already exists!"
                      .format(shelf=shelf_key))

    def get_shelf(self, shelf_name):
        """Return a shelf instance by supplying its name."""
        try:
            return self._shelves[shelf_name]
        except KeyError:
            print("Shelf named {shelf} not found in {library}"
                  .format(shelf=shelf_name, library=self.name))

    def report_all_shelves(self):
        """Print a list of all shelves."""
        for shelf in self._shelves:
            print(shelf)

    def report_all_books(self):
        """Pretty print all books in the library."""
        print("= All Books at {library} =".format(library=self))
        print("+ {:^30} | {:^30} | {:^10} +"
              .format("Title", "Author", "Copies"))
        for shelf in self._shelves.itervalues():
            print("Shelf - {shelf}".format(shelf=shelf))
            shelf.report_books()


class Shelf(object):
    def __init__(self, name=""):
        self.name = name
        self._books = {}

    def __str__(self):
        return "{}".format(self.name)

    def get_book(self, title):
        """Retrieve a Book instance from the shelf by title."""
        if title in self._books:
            return self._books[title]
        else:
            print("{title} not found in {shelf}!"
                  .format(title=title, shelf=self.name))

    def add_books(self, *args):
        """Add any number of book instances to the shelf. Can also accept
        non-Book objects, which will be stringified into a new book's title.
        """
        for book in args:
            if isinstance(book, Book):
                book_key = book.title
                book_to_add = book
            else:
                book_key = str(book).title()
                book_to_add = Book(book_key)

            if book_key in self._books:
                self._books[book_key].add_copy()
            else:
                self._books[book_key] = book_to_add

    def remove_book(self, title):
        """Remove a book instance from the shelf."""
        if title in self._books:
            del self._books[title]
        else:
            print("{title} not found in {shelf}!"
                  .format(title=title, shelf=self.name))

    def report_books(self):
        """Print all books in the shelf with their information."""
        for book in self._books.itervalues():
            print(book.report())


class Book(object):
    def __init__(self, title, author="", page_count=0, desc="", copies=1):
        self.title = title
        self.author = author
        self.page_count = page_count
        self.desc = desc
        self._copies = self._maxcopies = copies

    def __str__(self):
        return ("Title: {title}\n"
                "Author: {author}\n"
                "Pages: {page_count}\n"
                "Copies: {copies}\n"
                "Description: {description}"
                .format(title=self.title, author=self.author,
                        page_count=self.page_count, copies=self.copy_str(),
                        description=self.desc))

    def copy_str(self):
        """Format a string reporting copy information."""
        return "{} / {}".format(self._copies, self._maxcopies)

    def report(self):
        """Format a string for purposes of printing important book info."""
        info = self.title, self.author, self.copy_str()
        return "+ {:<30} | {:<30} | {:^10} +".format(*info)

    def enshelf(self, shelf):
        """Add book to a Shelf instance."""
        shelf.add_book(self)

    def unshelf(self, shelf):
        """Remove book from a Shelf instance."""
        shelf.remove_book(self)

    def add_copy(self):
        """Add a duplicate copy of this book to allow more checkouts."""
        self._copies += 1
        self._maxcopies += 1

    def report_copies(self):
        """Report how many copies of this book are available."""
        print("{title} now has {copies} copies."
              .format(title=self.title, copies=self.copy_str()))

    def check_out(self):
        """Check out a copy of the book."""
        if self._copies:
            self._copies -= 1
            self.report_copies()
        else:
            print("Cannot check out {title}: no more copies!"
                  .format(title=self.title))

    def check_in(self):
        """Check in a copy of the book."""
        if self._copies < self._maxcopies:
            self._copies += 1
            self.report_copies()
        else:
            print("All copies of {title} already accounted for!"
                  .format(title=self.title))


if __name__ == "__main__":
    # Create a library with a name
    library = Library("Bellevue Public Library")

    # Shelves can be created as their own instances...
    shelf1 = Shelf("Fantasy")
    shelf2 = Shelf("Science Fiction")

    # ... or by passing a string to the library's add method
    library.add_shelves(shelf1, shelf2, "Boring Adult Stuff")

    # A book can be created with all information up front
    book1 = Book(title="A Game of Thrones",
                 author="George R. R. Martin",
                 page_count=864,
                 desc="Here is the first volume in George R. R. Martin's "
                      "cycle of novels that includes A Clash of Kings and A "
                      "Storm of Swords.",
                 copies=2)

    # Or just with a title
    book2 = Book("The Lord of the Rings")

    # Like shelves, a string passed to the add method will also create a book
    shelf1.add_books(book1, book2, "The Scar")

    # A book can be retrieved at the shelf level
    book3 = shelf1.get_book("The Scar")

    # Which allows the book's information to be added / updated later
    book3.author = "China Mieville"
    book3.page_count = 608
    book3.description = ("In the third book in an astounding, genre-breaking "
                         "run, China Mieville expands the horizon beyond the "
                         "boundaries of New Crobuzon, setting sail on the "
                         "high seas of his ever-growing world of Bas Lag.")

    # Patrons can check out books, which updates the book's copy count
    book1.check_out()

    # Checking out a book with no copies left is not allowed
    book2.check_out()
    book2.check_out()

    # Patrons can check a book back in
    book2.check_in()

    # Adding a book with the same title to a shelf will add a copy
    shelf1.add_books("The Scar")

    # Copy information can be seen in the library's book reporting output
    library.report_all_books()