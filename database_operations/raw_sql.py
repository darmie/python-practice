"""
Raw SQL Query Examples

Demonstrates using raw SQL with SQLAlchemy and sqlite3.
"""
import sqlite3
from typing import List, Dict, Any, Optional
from sqlalchemy import text
from sqlalchemy.orm import Session


class RawSQLQueries:
    """Examples using raw SQL queries."""

    def __init__(self, session: Session):
        self.session = session

    def execute_raw_query(self, query: str, params: Optional[Dict] = None) -> List[Dict]:
        """
        Execute raw SQL query and return results as list of dictionaries.

        Example:
            >>> queries = RawSQLQueries(session)
            >>> result = queries.execute_raw_query(
            ...     "SELECT * FROM users WHERE username = :username",
            ...     {"username": "alice"}
            ... )
        """
        result = self.session.execute(text(query), params or {})
        columns = result.keys()
        return [dict(zip(columns, row)) for row in result.fetchall()]

    def get_users_with_post_count(self) -> List[Dict]:
        """Get users with their post count using raw SQL."""
        query = """
            SELECT u.id, u.username, u.email, COUNT(p.id) as post_count
            FROM users u
            LEFT JOIN posts p ON u.id = p.author_id
            GROUP BY u.id, u.username, u.email
            ORDER BY post_count DESC
        """
        return self.execute_raw_query(query)

    def get_products_by_category(self, category: str) -> List[Dict]:
        """Get products by category using parameterized query."""
        query = """
            SELECT id, name, price, stock
            FROM products
            WHERE category = :category
            ORDER BY price DESC
        """
        return self.execute_raw_query(query, {"category": category})

    def get_expensive_products(self, min_price: float) -> List[Dict]:
        """Get products above a certain price."""
        query = """
            SELECT name, price, stock, (price * stock) as total_value
            FROM products
            WHERE price >= :min_price
            ORDER BY total_value DESC
        """
        return self.execute_raw_query(query, {"min_price": min_price})

    def search_posts(self, keyword: str) -> List[Dict]:
        """Full-text search in posts."""
        query = """
            SELECT p.id, p.title, p.content, u.username as author
            FROM posts p
            JOIN users u ON p.author_id = u.id
            WHERE p.title LIKE :keyword OR p.content LIKE :keyword
        """
        return self.execute_raw_query(query, {"keyword": f"%{keyword}%"})


class SQLiteConnection:
    """
    Direct SQLite connection handler (without ORM).

    Example:
        >>> db = SQLiteConnection('example.db')
        >>> db.execute("INSERT INTO users (username, email) VALUES (?, ?)",
        ...            ('john', 'john@example.com'))
        >>> users = db.query("SELECT * FROM users")
    """

    def __init__(self, database: str):
        self.database = database
        self.connection: Optional[sqlite3.Connection] = None

    def connect(self):
        """Establish database connection."""
        self.connection = sqlite3.connect(self.database)
        self.connection.row_factory = sqlite3.Row  # Return rows as dictionaries
        return self.connection

    def close(self):
        """Close database connection."""
        if self.connection:
            self.connection.close()

    def execute(self, query: str, params: tuple = ()) -> int:
        """
        Execute a query (INSERT, UPDATE, DELETE).

        Returns:
            Number of affected rows
        """
        if not self.connection:
            self.connect()

        cursor = self.connection.cursor()
        cursor.execute(query, params)
        self.connection.commit()
        return cursor.rowcount

    def query(self, query: str, params: tuple = ()) -> List[Dict]:
        """
        Execute a SELECT query.

        Returns:
            List of dictionaries
        """
        if not self.connection:
            self.connect()

        cursor = self.connection.cursor()
        cursor.execute(query, params)
        columns = [description[0] for description in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def query_one(self, query: str, params: tuple = ()) -> Optional[Dict]:
        """
        Execute a SELECT query and return first result.

        Returns:
            Dictionary or None
        """
        results = self.query(query, params)
        return results[0] if results else None

    def executemany(self, query: str, params_list: List[tuple]) -> int:
        """
        Execute query with multiple parameter sets.

        Returns:
            Number of affected rows
        """
        if not self.connection:
            self.connect()

        cursor = self.connection.cursor()
        cursor.executemany(query, params_list)
        self.connection.commit()
        return cursor.rowcount


def create_database_with_raw_sql():
    """
    Example of creating a database schema using raw SQL.
    """
    db = SQLiteConnection(':memory:')  # In-memory database
    db.connect()

    # Create tables
    db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    db.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            author_id INTEGER NOT NULL,
            views INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (author_id) REFERENCES users(id)
        )
    """)

    # Insert sample data
    user_data = [
        ('alice', 'alice@example.com'),
        ('bob', 'bob@example.com'),
        ('charlie', 'charlie@example.com')
    ]

    db.executemany(
        "INSERT INTO users (username, email) VALUES (?, ?)",
        user_data
    )

    # Insert posts
    post_data = [
        ('First Post', 'Hello World!', 1),
        ('Python Tips', 'Python is great', 1),
        ('SQL Guide', 'Learning SQL', 2)
    ]

    db.executemany(
        "INSERT INTO posts (title, content, author_id) VALUES (?, ?, ?)",
        post_data
    )

    # Query data
    users = db.query("SELECT * FROM users")
    print(f"Created {len(users)} users")

    # Join query
    posts_with_authors = db.query("""
        SELECT p.title, p.content, u.username as author
        FROM posts p
        JOIN users u ON p.author_id = u.id
    """)

    print(f"Found {len(posts_with_authors)} posts")

    for post in posts_with_authors:
        print(f"  - {post['title']} by {post['author']}")

    db.close()


def prepared_statements_example():
    """
    Example of using prepared statements to prevent SQL injection.
    """
    db = SQLiteConnection(':memory:')
    db.connect()

    # Create table
    db.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            email TEXT
        )
    """)

    # UNSAFE: Direct string interpolation (vulnerable to SQL injection)
    # NEVER DO THIS:
    # username = "admin'; DROP TABLE users; --"
    # query = f"SELECT * FROM users WHERE username = '{username}'"

    # SAFE: Using parameterized queries
    username = "admin"
    safe_query = "SELECT * FROM users WHERE username = ?"
    result = db.query(safe_query, (username,))

    # Also safe: Named parameters
    safe_query_named = "SELECT * FROM users WHERE username = :username"
    # Note: For sqlite3 with named params, use dict instead
    cursor = db.connection.cursor()
    cursor.execute(safe_query_named, {"username": username})

    db.close()


if __name__ == '__main__':
    print("Creating database with raw SQL...")
    create_database_with_raw_sql()

    print("\nPrepared statements example:")
    prepared_statements_example()
    print("Done!")
