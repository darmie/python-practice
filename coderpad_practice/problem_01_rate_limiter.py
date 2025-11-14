"""
Problem: Implement a Rate Limiter

Design and implement a rate limiter that limits the number of requests
a user can make within a time window.

Requirements:
1. Support multiple users
2. Sliding window implementation
3. Thread-safe operations
4. Configurable rate and window

Example Usage:
    limiter = RateLimiter(max_requests=5, window_seconds=60)

    # User makes requests
    limiter.allow_request(user_id="user1")  # True
    limiter.allow_request(user_id="user1")  # True
    # ... 3 more times ...
    limiter.allow_request(user_id="user1")  # False (limit reached)

Difficulty: Medium
Time: 30-45 minutes
Focus: System design, data structures, concurrency
"""

import time
from collections import defaultdict, deque
from threading import Lock
from typing import Dict, Deque


class RateLimiter:
    """
    Rate limiter using sliding window algorithm.

    Implements a token bucket style rate limiter that tracks
    request timestamps and allows requests within configured limits.
    """

    def __init__(self, max_requests: int, window_seconds: int):
        """
        Initialize rate limiter.

        Args:
            max_requests: Maximum number of requests allowed in window
            window_seconds: Time window in seconds
        """
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.user_requests: Dict[str, Deque[float]] = defaultdict(deque)
        self.lock = Lock()

    def allow_request(self, user_id: str) -> bool:
        """
        Check if request is allowed for user.

        Args:
            user_id: Unique user identifier

        Returns:
            True if request is allowed, False otherwise
        """
        with self.lock:
            current_time = time.time()
            user_queue = self.user_requests[user_id]

            # Remove expired timestamps
            while user_queue and current_time - user_queue[0] >= self.window_seconds:
                user_queue.popleft()

            # Check if under limit
            if len(user_queue) < self.max_requests:
                user_queue.append(current_time)
                return True

            return False

    def get_remaining_requests(self, user_id: str) -> int:
        """
        Get number of remaining requests for user.

        Args:
            user_id: Unique user identifier

        Returns:
            Number of requests remaining
        """
        with self.lock:
            current_time = time.time()
            user_queue = self.user_requests[user_id]

            # Remove expired timestamps
            while user_queue and current_time - user_queue[0] >= self.window_seconds:
                user_queue.popleft()

            return max(0, self.max_requests - len(user_queue))

    def reset_user(self, user_id: str) -> None:
        """Reset rate limit for a user."""
        with self.lock:
            if user_id in self.user_requests:
                del self.user_requests[user_id]


# Alternative implementation: Token Bucket
class TokenBucketRateLimiter:
    """
    Rate limiter using token bucket algorithm.

    More memory efficient for high-frequency use cases.
    """

    def __init__(self, max_tokens: int, refill_rate: float):
        """
        Initialize token bucket rate limiter.

        Args:
            max_tokens: Maximum tokens in bucket
            refill_rate: Tokens added per second
        """
        self.max_tokens = max_tokens
        self.refill_rate = refill_rate
        self.buckets: Dict[str, Dict] = {}
        self.lock = Lock()

    def allow_request(self, user_id: str) -> bool:
        """Check if request is allowed."""
        with self.lock:
            current_time = time.time()

            if user_id not in self.buckets:
                self.buckets[user_id] = {
                    'tokens': self.max_tokens,
                    'last_refill': current_time
                }

            bucket = self.buckets[user_id]

            # Refill tokens
            time_passed = current_time - bucket['last_refill']
            tokens_to_add = time_passed * self.refill_rate
            bucket['tokens'] = min(
                self.max_tokens,
                bucket['tokens'] + tokens_to_add
            )
            bucket['last_refill'] = current_time

            # Try to consume token
            if bucket['tokens'] >= 1:
                bucket['tokens'] -= 1
                return True

            return False


# Test cases
if __name__ == '__main__':
    print("Testing Rate Limiter...")

    # Test 1: Basic rate limiting
    limiter = RateLimiter(max_requests=3, window_seconds=2)

    print("\nTest 1: Basic rate limiting (3 requests per 2 seconds)")
    for i in range(5):
        allowed = limiter.allow_request("user1")
        remaining = limiter.get_remaining_requests("user1")
        print(f"Request {i+1}: {'Allowed' if allowed else 'Blocked'} (Remaining: {remaining})")

    # Test 2: Multiple users
    print("\nTest 2: Multiple users")
    limiter2 = RateLimiter(max_requests=2, window_seconds=3)

    print("User1 requests:")
    for i in range(3):
        allowed = limiter2.allow_request("user1")
        print(f"  Request {i+1}: {'Allowed' if allowed else 'Blocked'}")

    print("User2 requests:")
    for i in range(3):
        allowed = limiter2.allow_request("user2")
        print(f"  Request {i+1}: {'Allowed' if allowed else 'Blocked'}")

    # Test 3: Token bucket
    print("\nTest 3: Token Bucket (5 tokens, 1 token/second)")
    token_limiter = TokenBucketRateLimiter(max_tokens=5, refill_rate=1.0)

    for i in range(7):
        allowed = token_limiter.allow_request("user1")
        print(f"Request {i+1}: {'Allowed' if allowed else 'Blocked'}")

    print("\nWaiting 2 seconds for token refill...")
    time.sleep(2)

    for i in range(3):
        allowed = token_limiter.allow_request("user1")
        print(f"After wait, request {i+1}: {'Allowed' if allowed else 'Blocked'}")
