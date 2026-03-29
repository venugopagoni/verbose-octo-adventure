# Prompts for wordnet.py Development

## Function: `__init__(self, synsets: str, hypernyms: str)`

```
Review the WordNet initialization process:
1. File handling robustness:
   - What happens if synsets or hypernyms file doesn't exist?
   - Should FileNotFoundError be caught and re-raised with context?
   - Consider encoding edge cases (UTF-8 vs other encodings)
2. DAG validation timing:
   - Is it efficient to build entire graph before validating DAG structure?
   - Consider early exit strategies if validation fails mid-construction
3. Resource management:
   - Memory footprint with large lexicons (1M+ synsets)
   - Consider lazy loading strategies for read-only operations
4. State initialization:
   - Validate that both hash tables are properly populated before SAP initialization
   - What guarantees should be documented about object state after init?
```

## Function: `_read_synsets(self, filename: str) -> int`

```
Analyze synset parsing and storage:
1. Data format handling:
   - Current assumption: comma-separated `id,synset_definition`
   - Handle edge cases: empty lines, malformed entries, missing commas
   - Support for escaped characters or special formatting?
2. Performance optimization:
   - Direct file I/O vs. buffering strategies
   - Dictionary lookups for duplicate nouns (repeated calls to __contains__)
   - Is pre-allocating list size beneficial?
3. Memory efficiency:
   - Store synset strings or references to reduce memory?
   - Consider interning strings for common words
4. Error recovery:
   - Skip malformed lines with logging or raise exception?
   - Validate synset_id uniqueness and contiguity (0 to V-1)
5. Return value:
   - Count accuracy - does it handle edge cases correctly?
   - Should return count or validate against expected vertex count?
```

## Function: `_read_hypernyms(self, filename: str, V: int) -> Digraph`

```
Evaluate hypernym graph construction:
1. File format validation:
   - Current: comma-separated `synset_id,hypernym1,hypernym2,...`
   - Handle empty lines and malformed entries
   - Validate all synset IDs are within [0, V-1] range
2. Edge case handling:
   - Synsets with no hypernyms (root nodes)
   - Synset IDs out of order or with gaps
   - Redundant or duplicate edges in input
3. Efficiency considerations:
   - Graph construction performance for large hypernym files
   - Any opportunities for batch edge addition?
4. Validation:
   - Should verify all synset IDs from synsets file are referenced?
   - What if hypernym file references non-existent synset IDs?
5. Return verification:
   - Confirm returned Digraph has expected edge count
   - Validate graph structure before passing to DAG validator
```

## Function: `_is_rooted_dag(self, G: Digraph) -> bool`

```
Analyze DAG validation algorithm:
1. Root node validation:
   - Current: exactly 1 node with outdegree 0
   - Is this the correct definition for WordNet hierarchy?
   - Should root be identified differently (no incoming edges vs. no outgoing)?
2. Cycle detection optimization:
   - DFS with on_stack tracking is sound, but review efficiency
   - Could use Tarjan's algorithm for stronger guarantees
   - What's the impact on large graphs (100K+ nodes)?
3. Edge cases:
   - Single node graph (is it valid rooted DAG?)
   - Disconnected components - should they be allowed?
   - Multiple roots with cycles below them
4. Performance:
   - Time complexity: O(V + E) - acceptable?
   - Space complexity for visited/on_stack arrays
   - Early-exit opportunities for large graphs?
5. Error messaging:
   - Distinguish between "multiple roots" vs. "contains cycle" in errors
   - Consider returning validation details for debugging
```

## Function: `_has_cycle(self, G: Digraph, v: int, visited, on_stack) -> bool`

```
Review DFS cycle detection:
1. Algorithm correctness:
   - Verify DFS with recursive backtracking correctly detects cycles
   - Test with various cycle configurations (self-loops, back edges)
2. Performance considerations:
   - Recursion depth for very deep graphs (stack overflow risk?)
   - Consider iterative DFS implementation as alternative
3. State management:
   - on_stack array usage for back-edge detection is correct?
   - Validate visited state tracking across multiple connected components
4. Edge cases:
   - Single node cycle (self-loop detection)
   - Nodes with multiple incoming edges
   - Very long paths without cycles
```

## Function: `nouns(self) -> Iterable[str]`

```
Evaluate public noun enumeration API:
1. Return value considerations:
   - Should return list, set, iterator, or dict_keys?
   - Memory implications for large lexicons
   - Thread-safety of returning mutable collection reference
2. Performance:
   - Is lazy evaluation (generator) better than direct keys()?
   - Cost of iterating vs. accessing specific nouns
3. Consistency:
   - Should return be sorted for deterministic ordering?
   - Document iteration order guarantees (or lack thereof)
4. Documentation:
   - Add examples of typical usage patterns
   - Specify if returned collection is live (reflects future changes)
```

## Function: `is_noun(self, word: str) -> bool`

```
Analyze noun membership checking:
1. Input validation:
   - Current: raises ValueError if word is None
   - Should also handle empty strings or whitespace?
   - Case sensitivity: should "horse" and "Horse" be treated differently?
2. Performance:
   - O(1) dictionary lookup is optimal
   - Any issues with Python's dict hashing for very large datasets?
3. Edge cases:
   - Special characters or Unicode in noun strings
   - Very long noun strings
4. API design:
   - Return False for None/empty instead of raising exception?
   - Document exact error conditions clearly
```

## Function: `distance(self, nounA: str, nounB: str) -> int`

```
Review semantic distance computation:
1. Input validation:
   - Current: checks both nouns exist before querying SAP
   - Behavior when nounA == nounB (should distance be 0?)
   - Handle None, empty string, or invalid nouns?
2. Algorithm correctness:
   - Verify SAP.length() returns correct shortest path length
   - What does SAP return for nouns with no common ancestor?
   - Edge case: nouns in different connected components
3. Performance optimization:
   - Current calls SAP.length(list_of_ids) for synset lists
   - Any caching strategy for repeated queries?
   - What's the cost of multi-source BFS in SAP?
4. Documentation:
   - Specify return value for nouns with no common ancestor (-1?)
   - Document time complexity: O(V + E) where E comes from SAP
   - Add usage examples
```

## Function: `sap(self, nounA: str, nounB: str) -> str`

```
Analyze Shortest Ancestral Path computation:
1. Correctness verification:
   - Does SAP.ancestor() return correct LCA (Lowest Common Ancestor)?
   - What if multiple common ancestors with equal distance exist?
   - Edge case: ancestor is nounA or nounB themselves
2. Performance:
   - Multi-source BFS implementation efficiency
   - Any optimization opportunities (memoization, preprocessing)?
3. Error handling:
   - What happens if ancestor_id is not in _id_to_synset?
   - Should validate ancestor_id exists before lookup
4. Return value:
   - Is synset string the most useful return format?
   - Consider returning synset ID or both ID and string
5. Documentation:
   - Explain what "ancestral path" means in WordNet context
   - Provide examples: "dog" ↔ "cat" → common ancestor "animal"
   - Clarify synset definition format in return value
```

## Integration & API Design

```
Review overall WordNet API design:
1. Public vs. private methods:
   - Are private methods (_read_*, _is_*, _has_*) implementation details?
   - Could they be useful public utilities? (likely not)
2. Consistency:
   - distance() and sap() both take two nouns - parallel API good
   - Error handling consistent across methods
3. Extensibility:
   - Could API support batch operations (multiple noun pairs)?
   - Consider returning structured objects vs. raw values
4. Documentation gaps:
   - Module docstring explaining WordNet structure
   - Class docstring with usage examples
   - API reference with parameter types and return values
```

## Testing Strategy

```
Design comprehensive test coverage for wordnet.py:
1. Initialization tests:
   - Valid synsets and hypernyms files
   - Missing files, malformed files, empty files
   - Invalid DAG (cycles, multiple roots, disconnected components)
2. Data parsing tests:
   - Correct noun-to-synset mapping
   - Correct hypernym graph structure
   - Edge cases: special characters, unicode, empty synsets
3. Lookup tests:
   - is_noun() for valid/invalid words
   - distance() accuracy for various noun pairs
   - sap() returns correct ancestor synsets
4. Performance tests:
   - Initialization time with large lexicons
   - Query response times (distance, sap)
   - Memory profiling with real WordNet datasets
5. Edge case tests:
   - Single noun, single synset, single root
   - Very deep hierarchies
   - Nouns with multiple synsets
```

## Performance Optimization

```
Propose enhancements to WordNet query performance:
1. Query caching:
   - Memoize distance() results for repeated pairs
   - Cache common ancestor queries
2. Preprocessing strategies:
   - Pre-compute all pairwise distances (trade-off: space vs. time)
   - Build secondary indices for faster lookups
3. Algorithmic improvements:
   - Consider LCA preprocessing (binary lifting, Tarjan's LCA)
   - Batch query optimization for multiple noun pairs
4. Memory optimization:
   - String interning for synset definitions
   - Reduce in-memory representation of DAG
```
