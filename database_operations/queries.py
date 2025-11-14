"""
Database Query Examples

Demonstrates various query patterns using SQLAlchemy.
"""
from sqlalchemy import func, and_, or_, desc, asc
from sqlalchemy.orm import Session
from typing import List, Optional
from .models import User, Post, Product, Student, Course


class UserRepository:
    """Repository pattern for User operations."""

    def __init__(self, session: Session):
        self.session = session

    def create(self, username: str, email: str) -> User:
        """Create a new user."""
        user = User(username=username, email=email)
        self.session.add(user)
        self.session.commit()
        return user

    def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        return self.session.query(User).filter(User.id == user_id).first()

    def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        return self.session.query(User).filter(User.username == username).first()

    def get_all(self, limit: int = 100) -> List[User]:
        """Get all users."""
        return self.session.query(User).limit(limit).all()

    def update(self, user_id: int, **kwargs) -> Optional[User]:
        """Update user fields."""
        user = self.get_by_id(user_id)
        if user:
            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)
            self.session.commit()
        return user

    def delete(self, user_id: int) -> bool:
        """Delete user."""
        user = self.get_by_id(user_id)
        if user:
            self.session.delete(user)
            self.session.commit()
            return True
        return False

    def search_by_email(self, email_pattern: str) -> List[User]:
        """Search users by email pattern."""
        return self.session.query(User).filter(
            User.email.like(f'%{email_pattern}%')
        ).all()

    def get_active_users(self) -> List[User]:
        """Get only active users."""
        return self.session.query(User).filter(User.is_active == True).all()


class PostRepository:
    """Repository pattern for Post operations."""

    def __init__(self, session: Session):
        self.session = session

    def create(self, title: str, content: str, author_id: int) -> Post:
        """Create a new post."""
        post = Post(title=title, content=content, author_id=author_id)
        self.session.add(post)
        self.session.commit()
        return post

    def get_by_id(self, post_id: int) -> Optional[Post]:
        """Get post by ID."""
        return self.session.query(Post).filter(Post.id == post_id).first()

    def get_by_author(self, author_id: int) -> List[Post]:
        """Get all posts by author."""
        return self.session.query(Post).filter(
            Post.author_id == author_id
        ).order_by(desc(Post.created_at)).all()

    def get_popular_posts(self, min_views: int = 100) -> List[Post]:
        """Get posts with minimum view count."""
        return self.session.query(Post).filter(
            Post.views >= min_views
        ).order_by(desc(Post.views)).all()

    def search_by_title(self, keyword: str) -> List[Post]:
        """Search posts by title keyword."""
        return self.session.query(Post).filter(
            Post.title.like(f'%{keyword}%')
        ).all()

    def increment_views(self, post_id: int) -> Optional[Post]:
        """Increment post view count."""
        post = self.get_by_id(post_id)
        if post:
            post.views += 1
            self.session.commit()
        return post


class ProductRepository:
    """Repository pattern for Product operations."""

    def __init__(self, session: Session):
        self.session = session

    def create(self, name: str, price: float, **kwargs) -> Product:
        """Create a new product."""
        product = Product(name=name, price=price, **kwargs)
        self.session.add(product)
        self.session.commit()
        return product

    def get_by_id(self, product_id: int) -> Optional[Product]:
        """Get product by ID."""
        return self.session.query(Product).filter(Product.id == product_id).first()

    def get_by_category(self, category: str) -> List[Product]:
        """Get products by category."""
        return self.session.query(Product).filter(
            Product.category == category
        ).all()

    def get_in_stock(self) -> List[Product]:
        """Get products that are in stock."""
        return self.session.query(Product).filter(Product.stock > 0).all()

    def get_by_price_range(self, min_price: float, max_price: float) -> List[Product]:
        """Get products within price range."""
        return self.session.query(Product).filter(
            and_(Product.price >= min_price, Product.price <= max_price)
        ).all()

    def get_low_stock(self, threshold: int = 10) -> List[Product]:
        """Get products with low stock."""
        return self.session.query(Product).filter(
            and_(Product.stock > 0, Product.stock <= threshold)
        ).all()

    def update_stock(self, product_id: int, quantity: int) -> Optional[Product]:
        """Update product stock."""
        product = self.get_by_id(product_id)
        if product:
            product.stock = quantity
            self.session.commit()
        return product


def aggregation_queries(session: Session):
    """
    Examples of aggregation queries.

    Args:
        session: SQLAlchemy session

    Returns:
        Dictionary with aggregation results
    """
    results = {}

    # Count users
    results['total_users'] = session.query(func.count(User.id)).scalar()

    # Count posts per user
    results['posts_per_user'] = session.query(
        User.username,
        func.count(Post.id).label('post_count')
    ).join(Post).group_by(User.id).all()

    # Average product price
    results['avg_price'] = session.query(func.avg(Product.price)).scalar()

    # Products per category
    results['products_per_category'] = session.query(
        Product.category,
        func.count(Product.id).label('count')
    ).group_by(Product.category).all()

    # Total stock value
    results['total_stock_value'] = session.query(
        func.sum(Product.price * Product.stock)
    ).scalar()

    return results


def join_queries(session: Session):
    """
    Examples of join queries.

    Args:
        session: SQLAlchemy session

    Returns:
        Dictionary with join query results
    """
    results = {}

    # Get users with their post count
    results['users_with_post_count'] = session.query(
        User.username,
        func.count(Post.id).label('post_count')
    ).outerjoin(Post).group_by(User.id).all()

    # Get posts with author information
    results['posts_with_authors'] = session.query(
        Post.title,
        User.username
    ).join(User).all()

    # Get students with their courses
    results['students_with_courses'] = session.query(
        Student.name,
        func.count(Course.id).label('course_count')
    ).outerjoin(Student.courses).group_by(Student.id).all()

    return results


def complex_queries(session: Session):
    """
    Examples of complex queries.

    Args:
        session: SQLAlchemy session

    Returns:
        Dictionary with complex query results
    """
    results = {}

    # Subquery: Users with more than 2 posts
    subq = session.query(
        Post.author_id,
        func.count(Post.id).label('post_count')
    ).group_by(Post.author_id).having(func.count(Post.id) > 2).subquery()

    results['prolific_authors'] = session.query(User).join(
        subq, User.id == subq.c.author_id
    ).all()

    # Complex filter: Products that are expensive OR have low stock
    results['attention_needed_products'] = session.query(Product).filter(
        or_(
            Product.price > 500,
            and_(Product.stock > 0, Product.stock < 5)
        )
    ).all()

    # Window function equivalent: Get top 3 products by price in each category
    from sqlalchemy import select
    results['top_products_per_category'] = session.query(
        Product
    ).order_by(Product.category, desc(Product.price)).all()

    return results


def transaction_example(session: Session):
    """
    Example of transaction handling.

    Args:
        session: SQLAlchemy session
    """
    try:
        # Start transaction (implicit)
        user = User(username='transactional_user', email='trans@example.com')
        session.add(user)

        # Multiple operations
        post = Post(title='Transaction Test', content='Testing', author=user)
        session.add(post)

        # Commit transaction
        session.commit()
        print("Transaction completed successfully")

    except Exception as e:
        # Rollback on error
        session.rollback()
        print(f"Transaction failed: {e}")
        raise


if __name__ == '__main__':
    from .models import DatabaseManager

    db = DatabaseManager('sqlite:///example.db')
    session = db.get_session()

    # Example: Use repositories
    user_repo = UserRepository(session)
    post_repo = PostRepository(session)

    # Get all users
    users = user_repo.get_all()
    print(f"Found {len(users)} users")

    # Get aggregations
    agg_results = aggregation_queries(session)
    print(f"Total users: {agg_results['total_users']}")
    print(f"Average product price: ${agg_results['avg_price']:.2f}")

    session.close()
