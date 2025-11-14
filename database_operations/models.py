"""
SQLAlchemy Models and ORM Examples
"""
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
from typing import List, Optional

Base = declarative_base()

# Many-to-many relationship table
student_course = Table(
    'student_course',
    Base.metadata,
    Column('student_id', Integer, ForeignKey('students.id')),
    Column('course_id', Integer, ForeignKey('courses.id'))
)


class User(Base):
    """
    User model demonstrating basic ORM.

    Example:
        >>> user = User(username='john_doe', email='john@example.com')
        >>> session.add(user)
        >>> session.commit()
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    # Relationship
    posts = relationship('Post', back_populates='author', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"


class Post(Base):
    """
    Post model demonstrating one-to-many relationship.
    """
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    content = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    views = Column(Integer, default=0)

    # Relationship
    author = relationship('User', back_populates='posts')

    def __repr__(self):
        return f"<Post(id={self.id}, title='{self.title}')>"


class Product(Base):
    """
    Product model for e-commerce example.
    """
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    category = Column(String(50))

    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', price={self.price})>"


class Student(Base):
    """
    Student model demonstrating many-to-many relationship.
    """
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True)
    gpa = Column(Float)

    # Many-to-many relationship
    courses = relationship('Course', secondary=student_course, back_populates='students')

    def __repr__(self):
        return f"<Student(id={self.id}, name='{self.name}')>"


class Course(Base):
    """
    Course model demonstrating many-to-many relationship.
    """
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True)
    code = Column(String(10), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    credits = Column(Integer, default=3)

    # Many-to-many relationship
    students = relationship('Student', secondary=student_course, back_populates='courses')

    def __repr__(self):
        return f"<Course(id={self.id}, code='{self.code}', name='{self.name}')>"


class DatabaseManager:
    """
    Database manager for handling connections and sessions.

    Example:
        >>> db = DatabaseManager('sqlite:///example.db')
        >>> db.create_tables()
        >>> session = db.get_session()
    """

    def __init__(self, database_url: str = 'sqlite:///test.db'):
        self.engine = create_engine(database_url, echo=False)
        self.Session = sessionmaker(bind=self.engine)

    def create_tables(self):
        """Create all tables."""
        Base.metadata.create_all(self.engine)

    def drop_tables(self):
        """Drop all tables."""
        Base.metadata.drop_all(self.engine)

    def get_session(self):
        """Get a new database session."""
        return self.Session()


def create_sample_data(session):
    """
    Create sample data for testing.

    Args:
        session: SQLAlchemy session
    """
    # Create users
    user1 = User(username='alice', email='alice@example.com')
    user2 = User(username='bob', email='bob@example.com')

    session.add_all([user1, user2])
    session.commit()

    # Create posts
    post1 = Post(title='First Post', content='Hello World!', author=user1)
    post2 = Post(title='Python Tips', content='Python is awesome', author=user1)
    post3 = Post(title='Database Guide', content='Learn SQL', author=user2)

    session.add_all([post1, post2, post3])
    session.commit()

    # Create products
    products = [
        Product(name='Laptop', description='High-performance laptop', price=999.99, stock=10, category='Electronics'),
        Product(name='Mouse', description='Wireless mouse', price=29.99, stock=50, category='Electronics'),
        Product(name='Desk', description='Standing desk', price=299.99, stock=5, category='Furniture'),
    ]

    session.add_all(products)
    session.commit()

    # Create students and courses
    student1 = Student(name='John Doe', email='john@university.edu', gpa=3.5)
    student2 = Student(name='Jane Smith', email='jane@university.edu', gpa=3.8)

    course1 = Course(code='CS101', name='Introduction to Programming', credits=3)
    course2 = Course(code='CS201', name='Data Structures', credits=4)
    course3 = Course(code='MATH101', name='Calculus I', credits=4)

    # Enroll students in courses
    student1.courses.extend([course1, course2, course3])
    student2.courses.extend([course1, course2])

    session.add_all([student1, student2, course1, course2, course3])
    session.commit()


if __name__ == '__main__':
    # Example usage
    db = DatabaseManager('sqlite:///example.db')
    db.create_tables()

    session = db.get_session()
    create_sample_data(session)

    print("Sample data created successfully!")
    session.close()
