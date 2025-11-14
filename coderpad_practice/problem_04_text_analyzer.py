"""
Problem: Text Analysis and Processing

Implement a text analyzer that provides various statistics and operations
on text input. This tests string manipulation, data structures, and algorithms.

Requirements:
1. Word frequency counting
2. Find top K most frequent words
3. Character frequency analysis
4. Sentence detection and analysis
5. Pattern matching and searching

Example:
    analyzer = TextAnalyzer()
    text = "Hello world. Hello Python. Python is great!"

    analyzer.word_count()  # 7
    analyzer.most_common_words(2)  # [('hello', 2), ('python', 2)]
    analyzer.average_word_length()  # 5.14

Difficulty: Easy-Medium
Time: 25-35 minutes
Focus: String processing, data structures, algorithms
"""

import re
from collections import Counter, defaultdict
from typing import List, Tuple, Dict


class TextAnalyzer:
    """
    Comprehensive text analysis tool.

    Provides various statistics and operations on text data.
    """

    def __init__(self, text: str = ""):
        """
        Initialize text analyzer.

        Args:
            text: Input text to analyze
        """
        self.text = text
        self._words_cache = None
        self._sentences_cache = None

    def set_text(self, text: str) -> None:
        """Update text and clear caches."""
        self.text = text
        self._words_cache = None
        self._sentences_cache = None

    def _get_words(self) -> List[str]:
        """Extract words from text (cached)."""
        if self._words_cache is None:
            # Remove punctuation and split
            words = re.findall(r'\b\w+\b', self.text.lower())
            self._words_cache = words
        return self._words_cache

    def _get_sentences(self) -> List[str]:
        """Extract sentences from text (cached)."""
        if self._sentences_cache is None:
            # Split on sentence terminators
            sentences = re.split(r'[.!?]+', self.text)
            self._sentences_cache = [s.strip() for s in sentences if s.strip()]
        return self._sentences_cache

    def word_count(self) -> int:
        """Get total word count."""
        return len(self._get_words())

    def unique_word_count(self) -> int:
        """Get count of unique words."""
        return len(set(self._get_words()))

    def character_count(self, include_spaces: bool = True) -> int:
        """
        Get character count.

        Args:
            include_spaces: Whether to include spaces

        Returns:
            Character count
        """
        if include_spaces:
            return len(self.text)
        return len(self.text.replace(' ', ''))

    def sentence_count(self) -> int:
        """Get sentence count."""
        return len(self._get_sentences())

    def average_word_length(self) -> float:
        """Calculate average word length."""
        words = self._get_words()
        if not words:
            return 0.0
        return sum(len(word) for word in words) / len(words)

    def average_sentence_length(self) -> float:
        """Calculate average sentence length in words."""
        sentences = self._get_sentences()
        if not sentences:
            return 0.0

        total_words = sum(
            len(re.findall(r'\b\w+\b', sentence))
            for sentence in sentences
        )
        return total_words / len(sentences)

    def word_frequency(self) -> Dict[str, int]:
        """
        Get word frequency distribution.

        Returns:
            Dictionary of word -> count
        """
        return dict(Counter(self._get_words()))

    def most_common_words(self, n: int = 10) -> List[Tuple[str, int]]:
        """
        Get N most common words.

        Args:
            n: Number of words to return

        Returns:
            List of (word, count) tuples
        """
        return Counter(self._get_words()).most_common(n)

    def least_common_words(self, n: int = 10) -> List[Tuple[str, int]]:
        """Get N least common words."""
        counter = Counter(self._get_words())
        return counter.most_common()[:-n-1:-1]

    def character_frequency(self) -> Dict[str, int]:
        """Get character frequency (excluding spaces)."""
        chars = [c.lower() for c in self.text if c.isalnum()]
        return dict(Counter(chars))

    def find_word(self, word: str, case_sensitive: bool = False) -> List[int]:
        """
        Find all positions of a word.

        Args:
            word: Word to find
            case_sensitive: Whether to match case

        Returns:
            List of starting positions
        """
        text = self.text if case_sensitive else self.text.lower()
        search_word = word if case_sensitive else word.lower()

        positions = []
        start = 0

        while True:
            pos = text.find(search_word, start)
            if pos == -1:
                break
            positions.append(pos)
            start = pos + 1

        return positions

    def find_pattern(self, pattern: str) -> List[str]:
        """
        Find all matches of regex pattern.

        Args:
            pattern: Regular expression pattern

        Returns:
            List of matches
        """
        return re.findall(pattern, self.text)

    def get_longest_words(self, n: int = 5) -> List[str]:
        """Get N longest words."""
        words = self._get_words()
        return sorted(set(words), key=len, reverse=True)[:n]

    def get_palindromes(self) -> List[str]:
        """Find all palindrome words."""
        words = self._get_words()
        return [word for word in set(words) if word == word[::-1] and len(word) > 1]

    def readability_score(self) -> float:
        """
        Calculate Flesch Reading Ease score.

        Higher scores indicate easier readability.
        90-100: Very easy
        60-70: Standard
        0-30: Very difficult
        """
        words = self.word_count()
        sentences = self.sentence_count()

        if words == 0 or sentences == 0:
            return 0.0

        # Count syllables (simplified: count vowel groups)
        syllables = sum(
            len(re.findall(r'[aeiouy]+', word))
            for word in self._get_words()
        )

        # Flesch Reading Ease formula
        score = 206.835 - 1.015 * (words / sentences) - 84.6 * (syllables / words)
        return max(0, min(100, score))

    def get_summary(self) -> Dict:
        """Get comprehensive text summary."""
        return {
            'total_characters': self.character_count(include_spaces=True),
            'total_characters_no_spaces': self.character_count(include_spaces=False),
            'total_words': self.word_count(),
            'unique_words': self.unique_word_count(),
            'total_sentences': self.sentence_count(),
            'average_word_length': round(self.average_word_length(), 2),
            'average_sentence_length': round(self.average_sentence_length(), 2),
            'readability_score': round(self.readability_score(), 2),
            'most_common_words': self.most_common_words(5)
        }


# Test cases
if __name__ == '__main__':
    print("Testing Text Analyzer...\n")

    # Sample text
    text = """
    Python is an amazing programming language. Python is widely used in data science,
    web development, and automation. Many developers love Python because it's simple
    and powerful. Python's simplicity makes it perfect for beginners!
    """

    analyzer = TextAnalyzer(text)

    # Test 1: Basic statistics
    print("Test 1: Basic Statistics")
    print(f"Total words: {analyzer.word_count()}")
    print(f"Unique words: {analyzer.unique_word_count()}")
    print(f"Total characters: {analyzer.character_count()}")
    print(f"Sentences: {analyzer.sentence_count()}")
    print(f"Average word length: {analyzer.average_word_length():.2f}")
    print(f"Average sentence length: {analyzer.average_sentence_length():.2f}\n")

    # Test 2: Word frequency
    print("Test 2: Most Common Words")
    for word, count in analyzer.most_common_words(5):
        print(f"  {word}: {count}")
    print()

    # Test 3: Find word positions
    print("Test 3: Find 'Python'")
    positions = analyzer.find_word("python")
    print(f"Found 'python' at positions: {positions}")
    print(f"Occurrences: {len(positions)}\n")

    # Test 4: Pattern matching
    print("Test 4: Find all capitalized words")
    capitalized = analyzer.find_pattern(r'\b[A-Z][a-z]+')
    print(f"Capitalized words: {capitalized}\n")

    # Test 5: Longest words
    print("Test 5: Longest words")
    longest = analyzer.get_longest_words(5)
    print(f"Longest words: {longest}\n")

    # Test 6: Character frequency
    print("Test 6: Top character frequencies")
    char_freq = analyzer.character_frequency()
    top_chars = sorted(char_freq.items(), key=lambda x: x[1], reverse=True)[:5]
    for char, count in top_chars:
        print(f"  '{char}': {count}")
    print()

    # Test 7: Readability score
    print("Test 7: Readability")
    score = analyzer.readability_score()
    print(f"Readability score: {score:.2f}")

    if score >= 90:
        print("  Level: Very easy to read")
    elif score >= 60:
        print("  Level: Standard reading level")
    else:
        print("  Level: Difficult to read")
    print()

    # Test 8: Complete summary
    print("Test 8: Complete Summary")
    summary = analyzer.get_summary()
    for key, value in summary.items():
        print(f"  {key}: {value}")
    print()

    # Test 9: Edge cases
    print("Test 9: Edge Cases")

    # Empty text
    analyzer.set_text("")
    print(f"Empty text word count: {analyzer.word_count()}")

    # Single word
    analyzer.set_text("Hello")
    print(f"Single word count: {analyzer.word_count()}")

    # Palindromes
    analyzer.set_text("A man, a plan, a canal: Panama! Radar and level are cool.")
    palindromes = analyzer.get_palindromes()
    print(f"Palindromes found: {palindromes}")
