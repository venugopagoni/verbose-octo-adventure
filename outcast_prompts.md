# Prompts for outcast.py Development

## Function: `__init__(self, wordnet: WordNet)`

```
Review the constructor implementation:
1. Validate that WordNet parameter is properly type-checked
2. Check if defensive copying of WordNet object is needed or if reference is sufficient
3. Consider if additional state validation should occur
4. Evaluate error messaging clarity for null/invalid inputs
5. Suggest improvements to initialization robustness
```

## Function: `outcast(self, nouns: List[str]) -> str`

```
Analyze the core outcast detection algorithm:
1. Time complexity: O(n²) - can this be optimized using memoization with SAP?
2. Validate edge cases:
   - Single noun in list
   - All nouns with equal distance
   - Nouns not in WordNet lexicon
   - Empty or None list handling
3. Consider caching distance calculations between repeated noun pairs
4. Propose algorithm optimization: bidirectional BFS in SAP for faster distance queries
5. Review input validation - should invalid nouns raise exception or skip silently?
6. Suggest performance improvements for large noun lists (100+ nouns)
```

## Function: `main` (CLI Entry Point)

```
Test and improve the command-line interface:
1. Validate argument parsing robustness:
   - Missing or incorrect number of arguments
   - File not found error handling
   - File reading exceptions (encoding, permissions)
2. Improve output formatting:
   - Consider adding timing metrics for large queries
   - Add success/failure counts for batch processing
   - Suggest verbosity levels for logging
3. Edge cases to handle:
   - Empty outcast files
   - Malformed noun lists in files
   - Path traversal security considerations
4. Recommend enhancements:
   - Support for multiple output formats (JSON, CSV)
   - Batch mode with progress indication
   - Option to show distance breakdown for each noun
```

## Integration Tests

```
Design test coverage for outcast.py:
1. Unit tests:
   - Valid noun list returns correct outcast
   - Verify distance calculation accuracy
   - Test with different list sizes
2. Error handling tests:
   - Invalid/non-existent nouns
   - Empty lists
   - Single noun lists
   - Duplicate nouns in list
3. Performance tests:
   - Benchmark with 10, 100, 1000 noun lists
   - Memory profiling for large batches
4. Integration tests:
   - Full workflow: WordNet → Outcast finder → result
   - File I/O with various encodings
```

## Performance Optimization

```
Propose algorithmic improvements:
1. Current approach: O(n²) distance calculations
   - Every noun pair queried separately
2. Optimization strategies:
   - Multi-source BFS: compute distances from all nouns in single pass
   - Cache SAP results for repeated queries
   - Batch distance computation
3. Memory vs. Speed trade-offs
4. Expected performance gains with proposed optimizations
```

## Type Safety & Documentation

```
Enhance code quality:
1. Add comprehensive docstrings to each method:
   - Parameter descriptions with types
   - Return value documentation
   - Exceptions that can be raised
   - Usage examples
2. Add type hints:
   - All parameters and return types
   - Consider Optional[] for nullable values
3. Validate WordNet methods being called:
   - is_noun() method existence
   - distance() method signature and behavior
```
