"""
Unit Tests for OOP Design Patterns

Run with: pytest testing/test_oop_design.py -v
"""
import pytest
from oop_design.design_patterns import (
    Singleton, AnimalFactory, Subject, ConcreteObserver,
    Sorter, QuickSortStrategy, BubbleSortStrategy,
    ConcreteComponent, ConcreteDecoratorA, ConcreteDecoratorB
)
from oop_design.library_system import Library, Member, Book, Librarian


class TestDesignPatterns:
    """Test cases for design patterns."""

    def test_singleton_pattern(self):
        """Test that Singleton returns same instance."""
        s1 = Singleton()
        s2 = Singleton()
        assert s1 is s2

    def test_factory_pattern(self):
        """Test factory pattern creates correct objects."""
        factory = AnimalFactory()

        dog = factory.create_animal("dog")
        assert dog is not None
        assert dog.speak() == "Woof!"

        cat = factory.create_animal("cat")
        assert cat is not None
        assert cat.speak() == "Meow!"

        unknown = factory.create_animal("unknown")
        assert unknown is None

    def test_observer_pattern(self):
        """Test observer pattern notifications."""
        subject = Subject()
        observer1 = ConcreteObserver("Observer1")
        observer2 = ConcreteObserver("Observer2")

        subject.attach(observer1)
        subject.attach(observer2)

        # Change state should notify all observers
        subject.set_state("New State")
        assert subject.get_state() == "New State"

        # Detach observer
        subject.detach(observer1)
        subject.set_state("Another State")

    def test_strategy_pattern(self):
        """Test strategy pattern with different algorithms."""
        data = [5, 2, 8, 1, 9]

        # Test with QuickSort strategy
        sorter = Sorter(QuickSortStrategy())
        result = sorter.sort(data)
        assert result == [1, 2, 5, 8, 9]

        # Change to BubbleSort strategy
        sorter.set_strategy(BubbleSortStrategy())
        result = sorter.sort(data)
        assert result == [1, 2, 5, 8, 9]

    def test_decorator_pattern(self):
        """Test decorator pattern."""
        component = ConcreteComponent()
        assert component.operation() == "ConcreteComponent"

        # Add first decorator
        decorated_a = ConcreteDecoratorA(component)
        assert decorated_a.operation() == "DecoratorA(ConcreteComponent)"

        # Add second decorator
        decorated_b = ConcreteDecoratorB(decorated_a)
        assert decorated_b.operation() == "DecoratorB(DecoratorA(ConcreteComponent))"


class TestLibrarySystem:
    """Test cases for Library Management System."""

    @pytest.fixture
    def library(self):
        """Fixture providing a library instance."""
        return Library("City Library")

    @pytest.fixture
    def member(self):
        """Fixture providing a member instance."""
        return Member("M001", "John Doe", "john@example.com")

    @pytest.fixture
    def book(self):
        """Fixture providing a book instance."""
        return Book("978-0-123456-78-9", "Python Programming", "Jane Smith", 2023)

    def test_library_creation(self, library):
        """Test library creation."""
        assert library is not None

    def test_member_creation(self, member):
        """Test member creation."""
        assert member.name == "John Doe"
        assert member.email == "john@example.com"
        assert member.can_borrow() is True

    def test_book_creation(self, book):
        """Test book creation."""
        assert book.title == "Python Programming"
        assert book.author == "Jane Smith"
        assert book.is_overdue() is False

    def test_book_checkout(self, book):
        """Test book checkout process."""
        assert book.checkout() is True
        assert book.is_overdue() is False

        # Cannot checkout again
        assert book.checkout() is False

    def test_book_return(self, book):
        """Test book return process."""
        book.checkout()
        assert book.return_book() is True

        # Cannot return if not checked out
        assert book.return_book() is False

    def test_library_add_book(self, library, book):
        """Test adding book to library."""
        library.add_book(book)
        found_book = library.find_book(book.isbn)
        assert found_book == book

    def test_library_register_member(self, library, member):
        """Test registering member."""
        library.register_member(member)
        found_member = library.get_member(member.person_id)
        assert found_member == member

    def test_checkout_workflow(self, library, member, book):
        """Test complete checkout workflow."""
        library.add_book(book)
        library.register_member(member)

        # Checkout book
        success = library.checkout_book(member.person_id, book.isbn)
        assert success is True
        assert book in member.borrowed_books

    def test_return_workflow(self, library, member, book):
        """Test complete return workflow."""
        library.add_book(book)
        library.register_member(member)

        # Checkout then return
        library.checkout_book(member.person_id, book.isbn)
        success = library.return_book(member.person_id, book.isbn)
        assert success is True
        assert book not in member.borrowed_books

    def test_member_borrow_limit(self):
        """Test member borrowing limit."""
        member = Member("M001", "John Doe", "john@example.com", max_books=2)

        book1 = Book("ISBN1", "Book 1", "Author 1", 2023)
        book2 = Book("ISBN2", "Book 2", "Author 2", 2023)
        book3 = Book("ISBN3", "Book 3", "Author 3", 2023)

        assert member.borrow_book(book1) is True
        assert member.borrow_book(book2) is True
        assert member.can_borrow() is False
        assert member.borrow_book(book3) is False

    def test_search_books(self, library):
        """Test book search functionality."""
        book1 = Book("ISBN1", "Python Programming", "Author 1", 2023)
        book2 = Book("ISBN2", "Java Programming", "Author 2", 2023)
        book3 = Book("ISBN3", "Python Data Science", "Author 3", 2023)

        library.add_book(book1)
        library.add_book(book2)
        library.add_book(book3)

        results = library.search_books("Python")
        assert len(results) == 2

        results = library.search_books("Java")
        assert len(results) == 1


class TestLibrarian:
    """Test cases for Librarian functionality."""

    def test_librarian_add_book(self):
        """Test librarian adding book to library."""
        library = Library("City Library")
        librarian = Librarian("L001", "Jane Admin", "jane@library.com", "EMP001")
        book = Book("ISBN", "New Book", "Author", 2023)

        librarian.add_book_to_library(library, book)
        assert library.find_book(book.isbn) == book

    def test_librarian_remove_book(self):
        """Test librarian removing book from library."""
        library = Library("City Library")
        librarian = Librarian("L001", "Jane Admin", "jane@library.com", "EMP001")
        book = Book("ISBN", "Book to Remove", "Author", 2023)

        library.add_book(book)
        librarian.remove_book_from_library(library, book.isbn)
        assert library.find_book(book.isbn) is None
