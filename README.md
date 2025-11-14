# Python Practice Repository

A comprehensive collection of Python projects and exercises covering different programming paradigms, algorithms, and software engineering concepts. This repository is designed for technical interview preparation and skill development.

## Repository Structure

```
python-practice/
├── algorithms_and_data_structures/  # Core CS algorithms and data structures
│   ├── arrays_and_strings.py       # Array/string manipulation
│   ├── linked_lists.py              # Linked list implementations
│   ├── trees_and_graphs.py          # Tree and graph algorithms
│   ├── sorting_and_searching.py     # Sorting and search algorithms
│   └── dynamic_programming.py       # DP problems
│
├── oop_design/                      # Object-oriented design patterns
│   ├── design_patterns.py           # Common design patterns
│   ├── library_system.py            # Library management system
│   └── parking_lot.py               # Parking lot system design
│
├── functional_programming/          # Functional programming concepts
│   ├── higher_order_functions.py    # HOFs and composition
│   ├── immutability.py              # Immutable data structures
│   └── lazy_evaluation.py           # Generators and lazy evaluation
│
├── api_development/                 # REST API examples
│   ├── basic_api.py                 # Flask REST API
│   ├── middleware.py                # API middleware patterns
│   └── api_client.py                # HTTP client examples
│
├── database_operations/             # Database interaction patterns
│   ├── models.py                    # SQLAlchemy ORM models
│   ├── queries.py                   # Complex query examples
│   └── raw_sql.py                   # Raw SQL operations
│
├── testing/                         # Testing examples
│   ├── test_algorithms.py           # Algorithm tests
│   ├── test_oop_design.py           # OOP pattern tests
│   ├── test_functional.py           # Functional programming tests
│   └── conftest.py                  # Pytest configuration
│
└── utils/                           # Common utilities
    └── helpers.py                   # Helper functions and decorators
```

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd python-practice
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Module Overview

### 1. Algorithms and Data Structures

Practice fundamental algorithms and data structures commonly tested in technical interviews.

**Key Topics:**
- Arrays and Strings (two-pointer, sliding window)
- Linked Lists (reversal, cycle detection)
- Trees and Graphs (BFS, DFS, traversals)
- Sorting and Searching (binary search, quicksort, mergesort)
- Dynamic Programming (knapsack, LCS, coin change)

**Example Usage:**
```python
from algorithms_and_data_structures.arrays_and_strings import two_sum

result = two_sum([2, 7, 11, 15], 9)
print(result)  # [0, 1]
```

### 2. Object-Oriented Programming

Learn design patterns and system design through practical examples.

**Key Topics:**
- Design Patterns (Singleton, Factory, Observer, Strategy, Decorator)
- System Design (Library Management, Parking Lot)
- SOLID Principles
- Inheritance and Polymorphism

**Example Usage:**
```python
from oop_design.library_system import Library, Member, Book

library = Library("City Library")
member = Member("M001", "John Doe", "john@example.com")
book = Book("ISBN", "Python Guide", "Author", 2024)

library.add_book(book)
library.register_member(member)
library.checkout_book(member.person_id, book.isbn)
```

### 3. Functional Programming

Master functional programming concepts in Python.

**Key Topics:**
- Higher-Order Functions (map, filter, reduce, compose)
- Pure Functions and Immutability
- Lazy Evaluation and Generators
- Function Composition and Currying

**Example Usage:**
```python
from functional_programming.higher_order_functions import compose, pipe

add_one = lambda x: x + 1
double = lambda x: x * 2

f = compose(double, add_one)
print(f(3))  # 8
```

### 4. API Development

Build RESTful APIs and understand HTTP client patterns.

**Key Topics:**
- REST API Design (Flask)
- Middleware and Authentication
- Request/Response Handling
- HTTP Client Implementation
- Error Handling and Retry Logic

**Running the API:**
```bash
python -m api_development.basic_api
```

**Testing with Client:**
```python
from api_development.api_client import TaskAPIClient

client = TaskAPIClient('http://localhost:5000')
tasks = client.get_tasks()
new_task = client.create_task('Learn Python', 'Practice coding')
```

### 5. Database Operations

Work with databases using ORM and raw SQL.

**Key Topics:**
- SQLAlchemy ORM Models
- Relationships (One-to-Many, Many-to-Many)
- Complex Queries and Joins
- Aggregations and Subqueries
- Raw SQL and Prepared Statements
- Repository Pattern

**Example Usage:**
```python
from database_operations.models import DatabaseManager, create_sample_data
from database_operations.queries import UserRepository

db = DatabaseManager('sqlite:///example.db')
db.create_tables()

session = db.get_session()
user_repo = UserRepository(session)

user = user_repo.create('alice', 'alice@example.com')
```

### 6. Testing

Comprehensive testing examples using pytest.

**Key Topics:**
- Unit Testing
- Fixtures and Parametrization
- Test Organization
- Mocking and Patching
- Code Coverage

**Running Tests:**
```bash
# Run all tests
pytest

# Run specific test file
pytest testing/test_algorithms.py -v

# Run with coverage
pytest --cov=. --cov-report=html

# Run only unit tests
pytest -m unit

# Skip slow tests
pytest -m "not slow"
```

## Practice Exercises

### For Beginners

1. Start with `algorithms_and_data_structures/arrays_and_strings.py`
2. Practice with linked lists in `linked_lists.py`
3. Learn basic OOP with `design_patterns.py`
4. Write tests for the functions you create

### For Intermediate

1. Implement tree and graph algorithms
2. Build the Library Management System from scratch
3. Create a REST API with authentication
4. Practice dynamic programming problems
5. Explore functional programming patterns

### For Advanced

1. Implement complex system designs (Parking Lot, etc.)
2. Optimize database queries for performance
3. Build a complete API with database integration
4. Write comprehensive test suites
5. Combine multiple paradigms in a single project

## Tips for Practice

1. **Understand Before Coding**: Read the problem carefully and plan your approach
2. **Test Driven Development**: Write tests first, then implement
3. **Time Yourself**: Practice solving problems within time limits
4. **Review Solutions**: After solving, review and optimize
5. **Learn Patterns**: Recognize common patterns and when to apply them
6. **Document Your Code**: Write clear docstrings and comments

## Common Assessment Patterns

### Algorithm Interviews
- Two-pointer technique
- Sliding window
- Binary search variations
- DFS/BFS on trees and graphs
- Dynamic programming states

### System Design
- Object-oriented principles
- Design patterns application
- Class relationships
- API design
- Database schema design

### Coding Best Practices
- Clean, readable code
- Proper error handling
- Type hints and documentation
- Unit tests
- Time and space complexity analysis

## Resources

### Documentation
- All functions include docstrings with examples
- Type hints for better IDE support
- Comments explaining complex logic

### Testing
- Comprehensive test coverage
- Examples of different testing patterns
- Fixtures for common test scenarios

## Code Quality

Run code quality tools:

```bash
# Format code
black .

# Lint code
flake8 .

# Type checking
mypy .
```

## Contributing

This is a practice repository. Feel free to:
- Add more practice problems
- Improve existing solutions
- Add more test cases
- Document patterns and approaches

## License

This repository is for educational purposes.

## Additional Notes

- All code includes examples in docstrings
- Functions are designed to be self-contained
- Tests demonstrate proper usage
- Focus on understanding concepts, not memorization
- Practice explaining your solutions out loud

Happy Coding!
