class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.available = True

    def display(self):
        status = "Available" if self.available else "Borrowed"
        print(f"Title: {self.title}, Author: {self.author}, Status: {status}")


class Patron:
    def __init__(self, name):
        self.name = name
        self.borrowed_books = []

    def display(self):
        print(f"Patron: {self.name}")
        if self.borrowed_books:
            print("Borrowed Books:")
            for book in self.borrowed_books:
                print(f"- {book.title}")
        else:
            print("No books borrowed.")


class Library:
    def __init__(self):
        self.books = []
        self.patrons = []

    def add_book(self, title, author):
        book = Book(title, author)
        self.books.append(book)
        print(f"Book '{title}' added successfully.")

    def register_patron(self, name):
        patron = Patron(name)
        self.patrons.append(patron)
        print(f"Patron '{name}' registered successfully.")

    def borrow_book(self, patron_name, book_title):
        patron = next((p for p in self.patrons if p.name == patron_name), None)
        book = next((b for b in self.books if b.title == book_title), None)

        if patron and book:
            if book.available:
                book.available = False
                patron.borrowed_books.append(book)
                print(f"{patron.name} borrowed '{book.title}'.")
            else:
                print("Book is already borrowed.")
        else:
            print("Patron or book not found.")

    def return_book(self, patron_name, book_title):
        patron = next((p for p in self.patrons if p.name == patron_name), None)

        if patron:
            for book in patron.borrowed_books:
                if book.title == book_title:
                    book.available = True
                    patron.borrowed_books.remove(book)
                    print(f"{patron.name} returned '{book.title}'.")
                    return
            print("Book not borrowed by this patron.")
        else:
            print("Patron not found.")

    def show_books(self):
        print("\nLibrary Books:")
        for book in self.books:
            book.display()

    def show_patrons(self):
        print("\nRegistered Patrons:")
        for patron in self.patrons:
            patron.display()


# Example Usage
library = Library()

# Adding books
library.add_book("Python Basics", "John Smith")
library.add_book("Data Structures", "Alice Brown")

# Registering patrons
library.register_patron("Riya")
library.register_patron("Rohit")

# Borrowing books
library.borrow_book("Riya", "Python Basics")

# Show books
library.show_books()

# Returning books
library.return_book("Riya", "Python Basics")

# Show updated data
library.show_books()