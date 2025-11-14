# CoderPad Practice Problems

Real-world coding problems commonly found in CoderPad technical assessments for senior Python developers.

## Problem Set Overview

These problems are designed to mirror actual CoderPad interview questions, focusing on:
- System design and architecture
- Algorithm optimization
- Real-world business logic
- Data structure selection
- Thread safety and concurrency
- Code quality and best practices

## Problems

### Problem 1: Rate Limiter
**File**: `problem_01_rate_limiter.py`
**Difficulty**: Medium
**Time**: 30-45 minutes

Implement a rate limiting system that controls request frequency per user.

**Key Concepts**:
- Sliding window algorithm
- Token bucket pattern
- Thread safety with locks
- Time-based data structures

**What Interviewers Look For**:
- Understanding of different rate limiting approaches
- Proper use of data structures (deque for sliding window)
- Thread-safe implementation
- Time complexity analysis

### Problem 2: LRU Cache
**File**: `problem_02_lru_cache.py`
**Difficulty**: Medium
**Time**: 30-40 minutes

Implement an LRU (Least Recently Used) cache with O(1) operations.

**Key Concepts**:
- HashMap + Doubly Linked List
- O(1) get and put operations
- Cache eviction policies
- Data structure design

**What Interviewers Look For**:
- Ability to combine multiple data structures
- Understanding of time/space complexity
- Clean abstraction and encapsulation
- Handling edge cases

### Problem 3: URL Shortener
**File**: `problem_03_url_shortener.py`
**Difficulty**: Medium
**Time**: 30-45 minutes

Design a URL shortening service like bit.ly or TinyURL.

**Key Concepts**:
- Base62 encoding
- Hash-based generation
- Collision handling
- Bi-directional mapping

**What Interviewers Look For**:
- System design thinking
- Understanding of encoding schemes
- Handling collisions gracefully
- Support for custom aliases
- Usage tracking

### Problem 4: Text Analyzer
**File**: `problem_04_text_analyzer.py`
**Difficulty**: Easy-Medium
**Time**: 25-35 minutes

Build a text analysis tool with various statistics and operations.

**Key Concepts**:
- String processing
- Regular expressions
- Counter and frequency analysis
- Caching for performance

**What Interviewers Look For**:
- String manipulation skills
- Proper use of regex
- Performance optimization (caching)
- Comprehensive edge case handling

### Problem 5: Inventory Management System
**File**: `problem_05_inventory_system.py`
**Difficulty**: Medium
**Time**: 35-45 minutes

Design an inventory management system for tracking products and orders.

**Key Concepts**:
- Business logic implementation
- Thread-safe operations
- Data modeling with dataclasses
- Report generation

**What Interviewers Look For**:
- Real-world system design
- Proper data modeling
- Thread safety awareness
- Business logic correctness
- Reporting and analytics

## How to Use These Problems

### For Practice

1. **Read the Problem Statement**: Understand requirements fully
2. **Plan Your Approach**: Think about data structures and algorithms
3. **Set a Timer**: Practice under realistic time constraints
4. **Implement**: Write clean, working code
5. **Test**: Run the provided test cases
6. **Review**: Compare with the solution, identify improvements

### Time Management

CoderPad interviews typically run 45-90 minutes:
- **5-10 minutes**: Understand problem and clarify
- **10-15 minutes**: Plan approach and discuss with interviewer
- **25-50 minutes**: Implement solution
- **10-15 minutes**: Test and debug
- **5-10 minutes**: Optimize and discuss trade-offs

### What Interviewers Evaluate

1. **Problem Solving**: Can you break down complex problems?
2. **Code Quality**: Clean, readable, well-organized code
3. **Communication**: Explain your thought process clearly
4. **Testing**: Consider edge cases and test thoroughly
5. **Optimization**: Understand time/space complexity
6. **Adaptability**: Handle requirement changes gracefully

## Common Patterns in CoderPad Assessments

### System Design Patterns
- Rate limiting and throttling
- Caching strategies (LRU, LFU)
- URL shortening/hashing
- Data aggregation and reporting
- Real-time statistics

### Algorithm Patterns
- Hash tables for O(1) lookups
- Queues for FIFO operations
- Stacks for LIFO operations
- Heaps for priority-based access
- Trees for hierarchical data

### Coding Best Practices
```python
# Good practices for CoderPad interviews:

# 1. Type hints
def process_data(items: List[int]) -> Dict[str, int]:
    pass

# 2. Docstrings
def calculate_total(values: List[float]) -> float:
    """
    Calculate total sum of values.

    Args:
        values: List of numeric values

    Returns:
        Total sum
    """
    return sum(values)

# 3. Error handling
def safe_divide(a: float, b: float) -> Optional[float]:
    if b == 0:
        return None
    return a / b

# 4. Clear variable names
user_count = len(users)  # Good
uc = len(users)          # Bad

# 5. Comments for complex logic
# Use sliding window to track requests in time window
while queue and current_time - queue[0] >= window_seconds:
    queue.popleft()
```

## Testing Your Solutions

Each problem includes test cases at the bottom. Run them:

```bash
# Run individual problem
python coderpad_practice/problem_01_rate_limiter.py

# Run all with pytest
pytest coderpad_practice/ -v
```

## Tips for Success

### Before the Interview
1. Practice typing code (not just reading)
2. Get comfortable with Python standard library
3. Review time/space complexity analysis
4. Practice explaining your approach out loud

### During the Interview
1. **Clarify requirements** before coding
2. **Think out loud** - share your reasoning
3. **Start simple** then optimize
4. **Test as you go** with small examples
5. **Communicate** about trade-offs

### Red Flags to Avoid
- Jumping to code without planning
- Silent coding (not explaining thought process)
- Ignoring edge cases
- No testing
- Not asking clarifying questions
- Overcomplicating the solution

## Difficulty Progression

**Start Here** (if new to these problems):
1. Problem 4: Text Analyzer (Easiest)
2. Problem 2: LRU Cache
3. Problem 1: Rate Limiter

**Next Level**:
4. Problem 3: URL Shortener
5. Problem 5: Inventory System

**Practice All** before your actual assessment.

## Additional Resources

### Python Standard Library
Know these well for CoderPad:
- `collections`: Counter, deque, defaultdict, OrderedDict
- `heapq`: Heap operations
- `itertools`: Iterator tools
- `functools`: Functional tools (lru_cache, partial)
- `re`: Regular expressions
- `datetime`: Time handling
- `threading`: Locks and thread safety

### Time Complexity Review
- O(1): Hash table lookup, array index access
- O(log n): Binary search, balanced tree operations
- O(n): Linear scan, single loop
- O(n log n): Efficient sorting (merge sort, quicksort)
- O(n²): Nested loops, bubble sort

## Mock Interview Setup

1. Choose a problem you haven't solved
2. Set a 45-minute timer
3. Use a minimal editor (like CoderPad's interface)
4. Explain your approach out loud
5. Write code while explaining
6. Test thoroughly
7. Discuss optimizations

## Next Steps

After completing these problems:
1. Implement variations (e.g., distributed rate limiter)
2. Add more features (e.g., LRU cache with TTL)
3. Optimize solutions (better time/space complexity)
4. Practice explaining solutions to others
5. Review main repository problems for more practice

Good luck with your CoderPad assessment!
