"""
HTTP Client Examples using requests library
"""
import requests
from typing import Dict, Optional, Any
import json


class APIClient:
    """
    Generic API client wrapper.

    Example:
        >>> client = APIClient('https://api.example.com')
        >>> response = client.get('/users/1')
        >>> print(response.json())
    """

    def __init__(self, base_url: str, api_key: Optional[str] = None):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()

        if api_key:
            self.session.headers.update({'X-API-Key': api_key})

        self.session.headers.update({'Content-Type': 'application/json'})

    def get(self, endpoint: str, params: Optional[Dict] = None) -> requests.Response:
        """Make GET request."""
        url = f"{self.base_url}{endpoint}"
        return self.session.get(url, params=params)

    def post(self, endpoint: str, data: Optional[Dict] = None) -> requests.Response:
        """Make POST request."""
        url = f"{self.base_url}{endpoint}"
        return self.session.post(url, json=data)

    def put(self, endpoint: str, data: Optional[Dict] = None) -> requests.Response:
        """Make PUT request."""
        url = f"{self.base_url}{endpoint}"
        return self.session.put(url, json=data)

    def delete(self, endpoint: str) -> requests.Response:
        """Make DELETE request."""
        url = f"{self.base_url}{endpoint}"
        return self.session.delete(url)

    def close(self):
        """Close the session."""
        self.session.close()


class TaskAPIClient:
    """
    Specific client for Task API.

    Example:
        >>> client = TaskAPIClient('http://localhost:5000')
        >>> tasks = client.get_tasks()
        >>> new_task = client.create_task('New task', 'Description')
    """

    def __init__(self, base_url: str):
        self.client = APIClient(base_url)

    def get_tasks(self, completed: Optional[bool] = None) -> Dict:
        """Get all tasks, optionally filtered by completion status."""
        params = {}
        if completed is not None:
            params['completed'] = str(completed).lower()

        response = self.client.get('/tasks', params=params)
        response.raise_for_status()
        return response.json()

    def get_task(self, task_id: int) -> Dict:
        """Get a specific task by ID."""
        response = self.client.get(f'/tasks/{task_id}')
        response.raise_for_status()
        return response.json()

    def create_task(self, title: str, description: str = '') -> Dict:
        """Create a new task."""
        data = {
            'title': title,
            'description': description
        }
        response = self.client.post('/tasks', data=data)
        response.raise_for_status()
        return response.json()

    def update_task(self, task_id: int, **kwargs) -> Dict:
        """Update a task."""
        response = self.client.put(f'/tasks/{task_id}', data=kwargs)
        response.raise_for_status()
        return response.json()

    def delete_task(self, task_id: int) -> Dict:
        """Delete a task."""
        response = self.client.delete(f'/tasks/{task_id}')
        response.raise_for_status()
        return response.json()

    def get_stats(self) -> Dict:
        """Get task statistics."""
        response = self.client.get('/tasks/stats')
        response.raise_for_status()
        return response.json()


def handle_api_errors_example():
    """
    Example of proper error handling with API requests.
    """
    client = APIClient('http://localhost:5000')

    try:
        response = client.get('/tasks')
        response.raise_for_status()  # Raise exception for 4xx/5xx status codes

        data = response.json()
        print(f"Success: {data}")

    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
        print(f"Status Code: {e.response.status_code}")
        print(f"Response: {e.response.text}")

    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the API")

    except requests.exceptions.Timeout:
        print("Error: Request timed out")

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

    finally:
        client.close()


def pagination_example(base_url: str, endpoint: str, page_size: int = 10):
    """
    Example of handling paginated API responses.
    """
    client = APIClient(base_url)
    page = 1
    all_results = []

    while True:
        params = {
            'page': page,
            'per_page': page_size
        }

        response = client.get(endpoint, params=params)
        response.raise_for_status()

        data = response.json()
        items = data.get('items', [])

        if not items:
            break

        all_results.extend(items)
        page += 1

    client.close()
    return all_results


def retry_with_backoff(
    func,
    max_retries: int = 3,
    backoff_factor: float = 1.0
) -> Any:
    """
    Retry a function with exponential backoff.

    Example:
        >>> response = retry_with_backoff(
        ...     lambda: requests.get('http://api.example.com/data'),
        ...     max_retries=3
        ... )
    """
    import time

    for attempt in range(max_retries):
        try:
            return func()
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                raise

            wait_time = backoff_factor * (2 ** attempt)
            print(f"Attempt {attempt + 1} failed. Retrying in {wait_time}s...")
            time.sleep(wait_time)


if __name__ == '__main__':
    # Example usage
    print("Task API Client Example")
    print("-" * 50)

    # Make sure the API is running first!
    client = TaskAPIClient('http://localhost:5000')

    try:
        # Get all tasks
        print("\nFetching all tasks...")
        tasks = client.get_tasks()
        print(f"Found {tasks['count']} tasks")

        # Create a new task
        print("\nCreating new task...")
        new_task = client.create_task(
            title="Test API Client",
            description="Testing the API client implementation"
        )
        print(f"Created task: {new_task}")

        # Get stats
        print("\nFetching stats...")
        stats = client.get_stats()
        print(f"Statistics: {stats}")

    except requests.exceptions.ConnectionError:
        print("\nError: Could not connect to API.")
        print("Make sure the API is running: python -m api_development.basic_api")
