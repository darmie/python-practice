"""
Dynamic Programming problems
"""
from typing import List


def fibonacci(n: int) -> int:
    """
    Calculate nth Fibonacci number using dynamic programming.

    Args:
        n: Position in Fibonacci sequence

    Returns:
        Fibonacci number at position n

    Example:
        >>> fibonacci(10)
        55
    """
    if n <= 1:
        return n

    dp = [0] * (n + 1)
    dp[1] = 1

    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]

    return dp[n]


def climbing_stairs(n: int) -> int:
    """
    Count ways to climb n stairs (1 or 2 steps at a time).

    Args:
        n: Number of stairs

    Returns:
        Number of distinct ways

    Example:
        >>> climbing_stairs(3)
        3
    """
    if n <= 2:
        return n

    dp = [0] * (n + 1)
    dp[1] = 1
    dp[2] = 2

    for i in range(3, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]

    return dp[n]


def coin_change(coins: List[int], amount: int) -> int:
    """
    Find minimum number of coins to make amount.

    Args:
        coins: List of coin denominations
        amount: Target amount

    Returns:
        Minimum number of coins or -1 if impossible

    Example:
        >>> coin_change([1, 2, 5], 11)
        3
    """
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0

    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i:
                dp[i] = min(dp[i], dp[i - coin] + 1)

    return dp[amount] if dp[amount] != float('inf') else -1


def longest_common_subsequence(text1: str, text2: str) -> int:
    """
    Find length of longest common subsequence.

    Args:
        text1: First string
        text2: Second string

    Returns:
        Length of LCS

    Example:
        >>> longest_common_subsequence("abcde", "ace")
        3
    """
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    return dp[m][n]


def max_subarray_sum(nums: List[int]) -> int:
    """
    Find maximum sum of contiguous subarray (Kadane's algorithm).

    Args:
        nums: List of integers

    Returns:
        Maximum subarray sum

    Example:
        >>> max_subarray_sum([-2, 1, -3, 4, -1, 2, 1, -5, 4])
        6
    """
    if not nums:
        return 0

    max_sum = current_sum = nums[0]

    for num in nums[1:]:
        current_sum = max(num, current_sum + num)
        max_sum = max(max_sum, current_sum)

    return max_sum


def knapsack_01(weights: List[int], values: List[int], capacity: int) -> int:
    """
    0/1 Knapsack problem.

    Args:
        weights: List of item weights
        values: List of item values
        capacity: Knapsack capacity

    Returns:
        Maximum value that can be obtained

    Example:
        >>> knapsack_01([1, 3, 4, 5], [1, 4, 5, 7], 7)
        9
    """
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(
                    values[i - 1] + dp[i - 1][w - weights[i - 1]],
                    dp[i - 1][w]
                )
            else:
                dp[i][w] = dp[i - 1][w]

    return dp[n][capacity]


def word_break(s: str, word_dict: List[str]) -> bool:
    """
    Check if string can be segmented into words from dictionary.

    Args:
        s: Input string
        word_dict: List of valid words

    Returns:
        True if string can be segmented, False otherwise

    Example:
        >>> word_break("leetcode", ["leet", "code"])
        True
    """
    word_set = set(word_dict)
    dp = [False] * (len(s) + 1)
    dp[0] = True

    for i in range(1, len(s) + 1):
        for j in range(i):
            if dp[j] and s[j:i] in word_set:
                dp[i] = True
                break

    return dp[len(s)]
