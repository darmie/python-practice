"""
API Middleware and Request/Response Handling
"""
from flask import Flask, request, jsonify
from functools import wraps
from typing import Callable
import time
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def timing_middleware(f: Callable) -> Callable:
    """
    Middleware to measure request processing time.

    Example:
        @app.route('/endpoint')
        @timing_middleware
        def endpoint():
            return jsonify({'message': 'Hello'})
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        start_time = time.time()
        result = f(*args, **kwargs)
        end_time = time.time()

        duration = end_time - start_time
        logger.info(f"Request to {request.path} took {duration:.4f} seconds")

        return result
    return decorated_function


def require_api_key(f: Callable) -> Callable:
    """
    Middleware to require API key authentication.

    Example:
        @app.route('/protected')
        @require_api_key
        def protected():
            return jsonify({'message': 'Access granted'})
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')

        if not api_key:
            return jsonify({'error': 'API key required'}), 401

        # In production, validate against database
        valid_keys = ['test-key-123', 'dev-key-456']

        if api_key not in valid_keys:
            return jsonify({'error': 'Invalid API key'}), 403

        return f(*args, **kwargs)
    return decorated_function


def validate_json(required_fields: list) -> Callable:
    """
    Middleware to validate JSON request body.

    Example:
        @app.route('/users', methods=['POST'])
        @validate_json(['name', 'email'])
        def create_user():
            data = request.get_json()
            return jsonify(data), 201
    """
    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not request.is_json:
                return jsonify({'error': 'Content-Type must be application/json'}), 400

            data = request.get_json()

            if not data:
                return jsonify({'error': 'Request body is required'}), 400

            missing_fields = [field for field in required_fields if field not in data]

            if missing_fields:
                return jsonify({
                    'error': 'Missing required fields',
                    'fields': missing_fields
                }), 400

            return f(*args, **kwargs)
        return decorated_function
    return decorator


def rate_limit(max_requests: int, window_seconds: int) -> Callable:
    """
    Simple rate limiting middleware.

    Example:
        @app.route('/api/data')
        @rate_limit(max_requests=10, window_seconds=60)
        def get_data():
            return jsonify({'data': 'some data'})
    """
    request_history = {}

    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Use IP as identifier (in production, use user ID)
            client_id = request.remote_addr
            current_time = time.time()

            if client_id not in request_history:
                request_history[client_id] = []

            # Remove old requests outside the window
            request_history[client_id] = [
                req_time for req_time in request_history[client_id]
                if current_time - req_time < window_seconds
            ]

            if len(request_history[client_id]) >= max_requests:
                return jsonify({
                    'error': 'Rate limit exceeded',
                    'retry_after': window_seconds
                }), 429

            request_history[client_id].append(current_time)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


@app.before_request
def log_request():
    """Log all incoming requests."""
    logger.info(f"{request.method} {request.path} from {request.remote_addr}")


@app.after_request
def add_cors_headers(response):
    """Add CORS headers to all responses."""
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, X-API-Key'
    return response


# Example routes using middleware
@app.route('/public')
@timing_middleware
def public_endpoint():
    """Public endpoint with timing."""
    return jsonify({'message': 'This is public'})


@app.route('/protected')
@require_api_key
@timing_middleware
def protected_endpoint():
    """Protected endpoint requiring API key."""
    return jsonify({'message': 'This is protected'})


@app.route('/users', methods=['POST'])
@validate_json(['name', 'email'])
@timing_middleware
def create_user():
    """Create user with validation."""
    data = request.get_json()
    return jsonify({
        'message': 'User created',
        'user': data
    }), 201


@app.route('/limited')
@rate_limit(max_requests=5, window_seconds=60)
def rate_limited_endpoint():
    """Rate limited endpoint."""
    return jsonify({'message': 'This endpoint is rate limited'})


if __name__ == '__main__':
    app.run(debug=True, port=5001)
