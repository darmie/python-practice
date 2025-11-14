"""
Problem: Design a URL Shortener

Design and implement a URL shortening service like bit.ly or tinyurl.

Requirements:
1. encode(long_url): Convert long URL to short code
2. decode(short_code): Retrieve original URL from short code
3. Short codes should be unique and consistent
4. Handle collisions
5. Support custom aliases (optional)
6. Track usage statistics (optional)

Example:
    shortener = URLShortener()
    short = shortener.encode("https://www.example.com/very/long/url")
    # Returns: "abc123"

    original = shortener.decode("abc123")
    # Returns: "https://www.example.com/very/long/url"

Difficulty: Medium
Time: 30-45 minutes
Focus: System design, hashing, encoding
"""

import hashlib
import string
import random
from typing import Optional, Dict
from collections import defaultdict


class URLShortener:
    """
    URL shortener using base62 encoding and counter.

    Uses a counter to generate unique IDs and encodes them
    in base62 for short, URL-safe codes.
    """

    def __init__(self, base_url: str = "http://short.url/"):
        """
        Initialize URL shortener.

        Args:
            base_url: Base URL for shortened links
        """
        self.base_url = base_url
        self.url_to_code: Dict[str, str] = {}
        self.code_to_url: Dict[str, str] = {}
        self.counter = 0
        self.stats = defaultdict(int)  # Track usage

        # Base62 characters (0-9, a-z, A-Z)
        self.chars = string.digits + string.ascii_lowercase + string.ascii_uppercase
        self.base = len(self.chars)

    def encode(self, long_url: str, custom_alias: Optional[str] = None) -> str:
        """
        Encode long URL to short code.

        Args:
            long_url: Original URL to shorten
            custom_alias: Optional custom short code

        Returns:
            Short code
        """
        # Return existing code if URL already shortened
        if long_url in self.url_to_code:
            return self.url_to_code[long_url]

        # Use custom alias if provided and available
        if custom_alias:
            if custom_alias in self.code_to_url:
                raise ValueError(f"Alias '{custom_alias}' already exists")
            short_code = custom_alias
        else:
            # Generate short code from counter
            short_code = self._encode_base62(self.counter)
            self.counter += 1

        # Store mappings
        self.url_to_code[long_url] = short_code
        self.code_to_url[short_code] = long_url

        return self.base_url + short_code

    def decode(self, short_url: str) -> Optional[str]:
        """
        Decode short URL to original URL.

        Args:
            short_url: Shortened URL or code

        Returns:
            Original URL if found, None otherwise
        """
        # Extract code from URL
        short_code = short_url.replace(self.base_url, "")

        if short_code in self.code_to_url:
            # Track usage
            self.stats[short_code] += 1
            return self.code_to_url[short_code]

        return None

    def get_stats(self, short_code: str) -> int:
        """Get usage statistics for a short code."""
        return self.stats.get(short_code, 0)

    def _encode_base62(self, num: int) -> str:
        """
        Encode number to base62 string.

        Args:
            num: Number to encode

        Returns:
            Base62 encoded string
        """
        if num == 0:
            return self.chars[0]

        result = []
        while num > 0:
            result.append(self.chars[num % self.base])
            num //= self.base

        return ''.join(reversed(result))

    def _decode_base62(self, s: str) -> int:
        """
        Decode base62 string to number.

        Args:
            s: Base62 string

        Returns:
            Decoded number
        """
        num = 0
        for char in s:
            num = num * self.base + self.chars.index(char)
        return num


class URLShortenerHash:
    """
    Alternative implementation using MD5 hashing.

    Uses hash of URL for generating short codes.
    Handles collisions with chaining.
    """

    def __init__(self, code_length: int = 6):
        """
        Initialize hash-based URL shortener.

        Args:
            code_length: Length of short code
        """
        self.code_length = code_length
        self.code_to_url: Dict[str, str] = {}
        self.url_to_code: Dict[str, str] = {}

    def encode(self, long_url: str) -> str:
        """Encode URL using hash."""
        # Return existing code if available
        if long_url in self.url_to_code:
            return self.url_to_code[long_url]

        # Generate hash
        hash_value = hashlib.md5(long_url.encode()).hexdigest()

        # Try to use first N characters
        short_code = hash_value[:self.code_length]

        # Handle collisions
        attempt = 0
        while short_code in self.code_to_url and self.code_to_url[short_code] != long_url:
            # Try next segment of hash
            start = self.code_length + attempt
            end = start + self.code_length

            if end > len(hash_value):
                # Ran out of hash, add random suffix
                short_code = hash_value[:self.code_length] + str(attempt)
            else:
                short_code = hash_value[start:end]

            attempt += 1

        # Store mappings
        self.code_to_url[short_code] = long_url
        self.url_to_code[long_url] = short_code

        return short_code

    def decode(self, short_code: str) -> Optional[str]:
        """Decode short code to URL."""
        return self.code_to_url.get(short_code)


# Test cases
if __name__ == '__main__':
    print("Testing URL Shortener...\n")

    # Test 1: Basic operations
    print("Test 1: Basic encode/decode")
    shortener = URLShortener()

    url1 = "https://www.example.com/very/long/url/path?param=value"
    short1 = shortener.encode(url1)
    print(f"Long URL: {url1}")
    print(f"Short URL: {short1}")

    decoded = shortener.decode(short1)
    print(f"Decoded: {decoded}")
    assert decoded == url1
    print("✓ Encode/decode successful\n")

    # Test 2: Multiple URLs
    print("Test 2: Multiple URLs")
    urls = [
        "https://github.com/user/repo",
        "https://stackoverflow.com/questions/12345",
        "https://docs.python.org/3/library/collections.html"
    ]

    for url in urls:
        short = shortener.encode(url)
        print(f"{url[:40]}... -> {short}")

    print()

    # Test 3: Custom alias
    print("Test 3: Custom alias")
    url = "https://mycompany.com/product"
    short = shortener.encode(url, custom_alias="product")
    print(f"URL: {url}")
    print(f"Custom short URL: {short}")
    print(f"Decoded: {shortener.decode(short)}\n")

    # Test 4: Duplicate URL
    print("Test 4: Duplicate URL returns same code")
    url = "https://duplicate.com"
    short1 = shortener.encode(url)
    short2 = shortener.encode(url)
    print(f"First encode: {short1}")
    print(f"Second encode: {short2}")
    assert short1 == short2
    print("✓ Same URL returns same code\n")

    # Test 5: Usage statistics
    print("Test 5: Usage statistics")
    url = "https://tracked.com"
    short = shortener.encode(url)
    code = short.replace(shortener.base_url, "")

    for i in range(5):
        shortener.decode(short)

    stats = shortener.get_stats(code)
    print(f"URL accessed {stats} times\n")

    # Test 6: Hash-based implementation
    print("Test 6: Hash-based implementation")
    hash_shortener = URLShortenerHash(code_length=6)

    url = "https://example.com/hash-test"
    short = hash_shortener.encode(url)
    print(f"URL: {url}")
    print(f"Short code: {short}")
    print(f"Decoded: {hash_shortener.decode(short)}")

    # Same URL should produce same hash
    short2 = hash_shortener.encode(url)
    assert short == short2
    print("✓ Consistent hashing\n")

    # Test 7: Collision handling
    print("Test 7: Many URLs (testing collisions)")
    shortener2 = URLShortener()

    for i in range(100):
        url = f"https://example.com/page/{i}"
        short = shortener2.encode(url)

    print(f"Successfully encoded 100 URLs")
    print(f"Codes used: 0 - {shortener2.counter - 1}")

    # Verify all URLs are retrievable
    all_valid = all(
        shortener2.decode(shortener2.encode(f"https://example.com/page/{i}"))
        == f"https://example.com/page/{i}"
        for i in range(100)
    )
    print(f"All URLs retrievable: {all_valid}")
