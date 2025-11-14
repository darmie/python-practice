"""
Pytest Configuration and Shared Fixtures

This file is automatically discovered by pytest and provides
shared fixtures and configuration for all tests.
"""
import pytest
from datetime import datetime


@pytest.fixture
def sample_data():
    """Fixture providing sample data for tests."""
    return {
        'users': [
            {'id': 1, 'name': 'Alice', 'email': 'alice@example.com'},
            {'id': 2, 'name': 'Bob', 'email': 'bob@example.com'},
        ],
        'posts': [
            {'id': 1, 'title': 'First Post', 'author_id': 1},
            {'id': 2, 'title': 'Second Post', 'author_id': 2},
        ]
    }


@pytest.fixture
def temp_file(tmp_path):
    """
    Fixture providing a temporary file path.
    tmp_path is a built-in pytest fixture.
    """
    file_path = tmp_path / "test_file.txt"
    file_path.write_text("test content")
    return file_path


@pytest.fixture(scope="session")
def test_timestamp():
    """
    Session-scoped fixture that runs once for entire test session.
    Useful for expensive setup operations.
    """
    return datetime.now().isoformat()


@pytest.fixture
def mock_api_response():
    """Fixture providing mock API response data."""
    return {
        'status': 'success',
        'data': {
            'id': 123,
            'message': 'Test successful'
        },
        'timestamp': '2024-01-01T00:00:00Z'
    }


# Pytest hooks for customization
def pytest_configure(config):
    """
    Pytest hook for initial configuration.
    Add custom markers here.
    """
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )


def pytest_collection_modifyitems(config, items):
    """
    Pytest hook to modify test items during collection.
    Can be used to add markers, skip tests, etc.
    """
    for item in items:
        # Automatically mark slow tests
        if "slow" in item.nodeid:
            item.add_marker(pytest.mark.slow)
