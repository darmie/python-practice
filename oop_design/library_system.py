"""
Library Management System - OOP Design Example

A practical example demonstrating OOP principles:
- Encapsulation
- Inheritance
- Polymorphism
- Abstraction
"""
from datetime import datetime, timedelta
from typing import List, Optional
from enum import Enum


class BookStatus(Enum):
    """Book availability status."""
    AVAILABLE = "available"
    CHECKED_OUT = "checked_out"
    RESERVED = "reserved"


class Person:
    """Base class for people in the system."""

    def __init__(self, person_id: str, name: str, email: str):
        self._person_id = person_id
        self._name = name
        self._email = email

    @property
    def person_id(self) -> str:
        return self._person_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def email(self) -> str:
        return self._email


class Member(Person):
    """Library member who can borrow books."""

    def __init__(self, person_id: str, name: str, email: str, max_books: int = 5):
        super().__init__(person_id, name, email)
        self._borrowed_books: List['Book'] = []
        self._max_books = max_books

    def can_borrow(self) -> bool:
        """Check if member can borrow more books."""
        return len(self._borrowed_books) < self._max_books

    def borrow_book(self, book: 'Book') -> bool:
        """Attempt to borrow a book."""
        if self.can_borrow() and book.status == BookStatus.AVAILABLE:
            self._borrowed_books.append(book)
            return True
        return False

    def return_book(self, book: 'Book') -> bool:
        """Return a borrowed book."""
        if book in self._borrowed_books:
            self._borrowed_books.remove(book)
            return True
        return False

    @property
    def borrowed_books(self) -> List['Book']:
        return self._borrowed_books.copy()


class Librarian(Person):
    """Librarian who manages the library."""

    def __init__(self, person_id: str, name: str, email: str, employee_id: str):
        super().__init__(person_id, name, email)
        self._employee_id = employee_id

    def add_book_to_library(self, library: 'Library', book: 'Book') -> None:
        """Add a book to the library."""
        library.add_book(book)

    def remove_book_from_library(self, library: 'Library', isbn: str) -> None:
        """Remove a book from the library."""
        library.remove_book(isbn)


class Book:
    """Represents a book in the library."""

    def __init__(self, isbn: str, title: str, author: str, publication_year: int):
        self._isbn = isbn
        self._title = title
        self._author = author
        self._publication_year = publication_year
        self._status = BookStatus.AVAILABLE
        self._due_date: Optional[datetime] = None

    @property
    def isbn(self) -> str:
        return self._isbn

    @property
    def title(self) -> str:
        return self._title

    @property
    def author(self) -> str:
        return self._author

    @property
    def status(self) -> BookStatus:
        return self._status

    @property
    def due_date(self) -> Optional[datetime]:
        return self._due_date

    def checkout(self, days: int = 14) -> bool:
        """Check out the book."""
        if self._status == BookStatus.AVAILABLE:
            self._status = BookStatus.CHECKED_OUT
            self._due_date = datetime.now() + timedelta(days=days)
            return True
        return False

    def return_book(self) -> bool:
        """Return the book."""
        if self._status == BookStatus.CHECKED_OUT:
            self._status = BookStatus.AVAILABLE
            self._due_date = None
            return True
        return False

    def is_overdue(self) -> bool:
        """Check if book is overdue."""
        if self._status == BookStatus.CHECKED_OUT and self._due_date:
            return datetime.now() > self._due_date
        return False

    def __str__(self) -> str:
        return f"{self._title} by {self._author} ({self._publication_year})"


class Library:
    """Library system managing books and members."""

    def __init__(self, name: str):
        self._name = name
        self._books: dict[str, Book] = {}
        self._members: dict[str, Member] = {}

    def add_book(self, book: Book) -> None:
        """Add a book to the library."""
        self._books[book.isbn] = book

    def remove_book(self, isbn: str) -> bool:
        """Remove a book from the library."""
        if isbn in self._books:
            del self._books[isbn]
            return True
        return False

    def find_book(self, isbn: str) -> Optional[Book]:
        """Find a book by ISBN."""
        return self._books.get(isbn)

    def search_books(self, query: str) -> List[Book]:
        """Search books by title or author."""
        query_lower = query.lower()
        return [
            book for book in self._books.values()
            if query_lower in book.title.lower() or query_lower in book.author.lower()
        ]

    def register_member(self, member: Member) -> None:
        """Register a new member."""
        self._members[member.person_id] = member

    def get_member(self, person_id: str) -> Optional[Member]:
        """Get a member by ID."""
        return self._members.get(person_id)

    def checkout_book(self, member_id: str, isbn: str) -> bool:
        """Process book checkout."""
        member = self.get_member(member_id)
        book = self.find_book(isbn)

        if member and book and member.can_borrow():
            if book.checkout():
                member.borrow_book(book)
                return True
        return False

    def return_book(self, member_id: str, isbn: str) -> bool:
        """Process book return."""
        member = self.get_member(member_id)
        book = self.find_book(isbn)

        if member and book:
            if member.return_book(book):
                book.return_book()
                return True
        return False

    def get_overdue_books(self) -> List[Book]:
        """Get all overdue books."""
        return [book for book in self._books.values() if book.is_overdue()]
