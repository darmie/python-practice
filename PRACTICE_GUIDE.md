# Practice Guide

This guide provides a structured approach to using this repository for technical assessment preparation.

## Week-by-Week Study Plan

### Week 1: Foundations
**Focus**: Arrays, Strings, and Basic Algorithms

**Daily Practice:**
- Day 1-2: Arrays and Two-Pointer Technique
  - Study: `arrays_and_strings.py`
  - Practice: two_sum, merge_sorted_arrays
  - Write tests for your implementations

- Day 3-4: String Manipulation
  - Study: reverse_string, is_palindrome
  - Practice: longest_substring_without_repeating
  - Solve 5 string problems on your own

- Day 5-6: Sorting and Searching
  - Study: `sorting_and_searching.py`
  - Implement: binary_search, quick_sort, merge_sort
  - Practice: search_in_rotated_array

- Day 7: Review and Testing
  - Run all tests: `pytest testing/test_algorithms.py`
  - Review mistakes and optimize solutions

### Week 2: Data Structures
**Focus**: Linked Lists, Trees, and Graphs

**Daily Practice:**
- Day 1-2: Linked Lists
  - Study: `linked_lists.py`
  - Practice: reverse_linked_list, detect_cycle
  - Implement merge_two_sorted_lists from scratch

- Day 3-4: Trees
  - Study: `trees_and_graphs.py`
  - Practice: All traversals (inorder, preorder, postorder, level-order)
  - Solve: max_depth, is_valid_bst

- Day 5-6: Graphs
  - Study: Graph class, BFS, DFS
  - Practice: has_cycle
  - Implement BFS/DFS from memory

- Day 7: Review
  - Mock interview: Solve 2 tree problems in 30 minutes
  - Review time complexity of all solutions

### Week 3: Advanced Algorithms
**Focus**: Dynamic Programming and Complex Problems

**Daily Practice:**
- Day 1-2: DP Fundamentals
  - Study: `dynamic_programming.py`
  - Practice: fibonacci, climbing_stairs
  - Understand memoization vs tabulation

- Day 3-4: DP Patterns
  - Study: coin_change, knapsack_01
  - Practice: longest_common_subsequence
  - Solve 3 DP problems independently

- Day 5-6: Complex Algorithms
  - Study: max_subarray_sum (Kadane's algorithm)
  - Practice: word_break
  - Combine multiple techniques in solutions

- Day 7: Mock Assessment
  - Timed practice: 3 problems in 60 minutes
  - Focus on explanation and optimization

### Week 4: Object-Oriented Design
**Focus**: Design Patterns and System Design

**Daily Practice:**
- Day 1-2: Design Patterns
  - Study: `design_patterns.py`
  - Implement: Singleton, Factory, Observer
  - Understand when to use each pattern

- Day 3-4: System Design - Library System
  - Study: `library_system.py`
  - Understand: Class relationships, inheritance
  - Practice: Extend the system with new features

- Day 5-6: System Design - Parking Lot
  - Study: `parking_lot.py`
  - Implement from scratch without looking
  - Add new vehicle types and features

- Day 7: OOP Review
  - Explain SOLID principles with examples
  - Design a new system (e.g., Hotel Booking)

### Week 5: Functional Programming
**Focus**: FP Concepts and Patterns

**Daily Practice:**
- Day 1-2: Higher-Order Functions
  - Study: `higher_order_functions.py`
  - Practice: compose, pipe, curry
  - Implement custom map, filter, reduce

- Day 3-4: Immutability
  - Study: `immutability.py`
  - Practice: Pure functions
  - Understand benefits and tradeoffs

- Day 5-6: Lazy Evaluation
  - Study: `lazy_evaluation.py`
  - Practice: Generators, infinite sequences
  - Implement custom iterators

- Day 7: FP Integration
  - Combine FP concepts in a project
  - Refactor OOP code using FP principles

### Week 6: APIs and Databases
**Focus**: Backend Development Skills

**Daily Practice:**
- Day 1-2: REST APIs
  - Study: `basic_api.py`
  - Run and test the API
  - Add new endpoints

- Day 3: API Middleware
  - Study: `middleware.py`
  - Implement: Authentication, rate limiting
  - Test with Postman or curl

- Day 4-5: Database Operations
  - Study: `models.py`, `queries.py`
  - Practice: Complex queries, joins
  - Implement repository pattern

- Day 6: Integration
  - Build API with database backend
  - Implement CRUD operations
  - Add error handling

- Day 7: Testing
  - Write integration tests
  - Test API endpoints
  - Verify database operations

### Week 7: Testing and Quality
**Focus**: Testing Best Practices

**Daily Practice:**
- Day 1-2: Unit Testing
  - Study: All test files
  - Practice: Writing test cases
  - Understand fixtures and parametrization

- Day 3-4: Test Coverage
  - Run: `pytest --cov`
  - Improve coverage to 90%+
  - Write tests for edge cases

- Day 5-6: TDD Practice
  - Write tests first
  - Implement to pass tests
  - Refactor with confidence

- Day 7: Quality Review
  - Run linters (flake8, black, mypy)
  - Fix all warnings
  - Document all functions

### Week 8: Mock Assessments
**Focus**: Simulation and Review

**Daily Practice:**
- Day 1-2: Algorithms Mock
  - Timed assessment: 5 problems in 90 minutes
  - Cover: Arrays, Linked Lists, Trees
  - Self-evaluate and review

- Day 3: OOP Mock
  - Design a complete system in 60 minutes
  - Explain design decisions
  - Identify improvements

- Day 4: Full-Stack Mock
  - Build API with database in 2 hours
  - Include tests
  - Deploy locally

- Day 5: Review Weak Areas
  - Focus on topics with mistakes
  - Redo difficult problems
  - Explain solutions clearly

- Day 6-7: Final Preparation
  - Review all notes
  - Practice explaining code
  - Prepare questions to ask

## Problem-Solving Framework

### 1. Understand the Problem (5 minutes)
- Read carefully
- Identify inputs and outputs
- Ask clarifying questions
- Consider edge cases

### 2. Plan the Solution (10 minutes)
- Discuss approach
- Consider data structures
- Estimate time/space complexity
- Outline algorithm steps

### 3. Implement (25 minutes)
- Write clean, readable code
- Use meaningful variable names
- Add comments for complex logic
- Handle edge cases

### 4. Test (10 minutes)
- Test with example inputs
- Test edge cases
- Verify time/space complexity
- Consider optimizations

### 5. Optimize (10 minutes)
- Identify bottlenecks
- Discuss trade-offs
- Implement improvements
- Re-test

## Common Patterns Checklist

### Array/String Patterns
- [ ] Two Pointers
- [ ] Sliding Window
- [ ] Fast & Slow Pointers
- [ ] Merge Intervals
- [ ] Cyclic Sort

### Tree Patterns
- [ ] BFS (Level Order)
- [ ] DFS (Inorder, Preorder, Postorder)
- [ ] Binary Search Tree Operations
- [ ] Path Finding
- [ ] Lowest Common Ancestor

### Graph Patterns
- [ ] BFS/DFS Traversal
- [ ] Cycle Detection
- [ ] Topological Sort
- [ ] Union Find
- [ ] Shortest Path

### DP Patterns
- [ ] 0/1 Knapsack
- [ ] Unbounded Knapsack
- [ ] Fibonacci Numbers
- [ ] Palindromic Subsequence
- [ ] Longest Common Substring

## Assessment Day Tips

### Before the Assessment
1. Review key concepts
2. Get good sleep
3. Prepare environment
4. Have water nearby
5. Close distractions

### During the Assessment
1. Read ALL instructions carefully
2. Manage time effectively
3. Start with easier problems
4. Don't get stuck on one problem
5. Leave time for review

### Communication Tips
1. Think out loud
2. Explain your approach
3. Ask questions when unclear
4. Discuss trade-offs
5. Be open to feedback

### Code Quality
1. Use meaningful names
2. Write modular code
3. Handle errors gracefully
4. Add type hints
5. Include docstrings

## Common Mistakes to Avoid

1. Not testing edge cases
2. Ignoring time complexity
3. Overcomplicating solutions
4. Not asking questions
5. Giving up too quickly
6. Not explaining reasoning
7. Writing messy code
8. Forgetting to test
9. Not considering memory
10. Skipping documentation

## Resources

### When Stuck
1. Review similar solved problems
2. Draw diagrams
3. Test with small inputs
4. Break down into smaller steps
5. Discuss approach out loud

### For More Practice
1. Solve variations of each problem
2. Optimize existing solutions
3. Implement in different paradigms
4. Teach concepts to others
5. Write detailed explanations

## Progress Tracking

Create a spreadsheet to track:
- Problems solved
- Time taken
- Difficulty level
- Topics covered
- Mistakes made
- Lessons learned

## Final Week Checklist

- [ ] Solved 100+ problems
- [ ] Confident with all data structures
- [ ] Can explain time/space complexity
- [ ] Comfortable with OOP design
- [ ] Understand functional concepts
- [ ] Can build REST APIs
- [ ] Proficient with databases
- [ ] Write comprehensive tests
- [ ] Code is clean and documented
- [ ] Practiced mock assessments

Good luck with your assessment preparation!
