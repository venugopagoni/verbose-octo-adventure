# Prompts for digraph.py Development

## Function: `__init__(self, V: int)`

```
Review the Digraph constructor initialization:
1. Input validation:
   - Current: rejects negative V values
   - Edge case: V = 0 (empty graph allowed?)
   - Should limit maximum V for memory safety?
2. Data structure efficiency:
   - Adjacency list: optimal for sparse graphs, verify with use cases
   - Indegree tracking: necessary for every graph operation?
   - Pre-allocation vs. lazy initialization trade-offs
3. Memory footprint:
   - O(V) space for empty digraph
   - What's acceptable V size? (1M vertices? 1B?)
   - Consider memory constraints for large graphs
4. State consistency:
   - Verify _adj and _indegree arrays properly aligned
   - All vertices initialized to valid state
5. Error messaging:
   - Is ValueError clear enough for invalid input?
   - Should include information about maximum supported V?
```

## Function: `V(self) -> int`

```
Analyze vertex count accessor:
1. Design decision:
   - Why store _V instead of computing from _adj length?
   - Return actual count vs. capacity - current approach stores capacity (correct)
2. Performance:
   - O(1) lookup is optimal
   - Used frequently in validation - good caching
3. Documentation:
   - Clarify this returns vertex capacity, not active vertices
   - Vertices are 0-indexed: [0, V-1]
4. Consistency:
   - Parallel to E() method - symmetric API design
```

## Function: `E(self) -> int`

```
Review edge count tracking:
1. Correctness:
   - _E incremented in add_edge() - is it ever decremented?
   - No remove_edge() method - document permanence of edges
   - Multi-edges allowed? (v→w twice adds duplicate)
2. Performance:
   - O(1) edge count query is optimal
   - Tracking _E in _add_edge is cleaner than scanning adjacency lists
3. Edge cases:
   - Self-loops (v→v): how handled? Should they be allowed/separate?
   - What if add_edge() is called multiple times same vertices?
4. API clarity:
   - Does E() return total added edges or unique edges?
   - Document if duplicates are counted multiple times
5. Alternative designs:
   - Could compute E() on demand by summing outdegrees? Trade-off analysis
   - Current O(1) approach is preferred for query efficiency
```

## Function: `_validate_vertex(self, v: int)`

```
Analyze vertex validation utility:
1. Correctness:
   - Range check: [0, _V-1] is correct 1-indexed convention
   - Error message includes valid range - good UX
2. Performance considerations:
   - Called on every add_edge, adj, indegree, outdegree
   - O(1) operation - acceptable overhead
   - Could this be inlined for hot path optimization?
3. Exception design:
   - ValueError appropriate for invalid input
   - Should message include call context (which operation failed)?
4. Edge cases:
   - None input - caught by comparison?
   - Negative numbers handled correctly
   - Large numbers beyond int range?
5. Usage pattern:
   - Called consistently before all vertex operations - good
   - Consider using decorators for automatic validation?
```

## Function: `add_edge(self, v: int, w: int)`

```
Review edge addition implementation:
1. Algorithm correctness:
   - Current: append w to v's adjacency list, increment indegree[w]
   - Order of operations: validate → append → update indegree - correct?
   - What if append succeeds but indegree update fails? (rare but possible)
2. Duplicate edges:
   - Current allows multiple v→w edges (duplicates in adjacency list)
   - Is this behavior intended or bug?
   - Should check for duplicates before appending?
3. Self-loops:
   - add_edge(v, v) allowed - creates self-loop
   - Is this valid for WordNet use case?
   - Indegree and outdegree both increment for same vertex
4. Performance:
   - append() is O(1) amortized
   - Array indegree update is O(1)
   - Overall O(1) edge addition is optimal
   - Could detect duplicate edges with O(degree) check
5. Error handling:
   - What if indegree array is corrupted? (shouldn't happen)
   - Validation catches out-of-range vertices
6. Transaction safety:
   - Edge added but validation failed midway - partial state
   - Consider atomic operations or rollback
```

## Function: `adj(self, v: int) -> list[int]`

```
Analyze adjacency list retrieval:
1. Return semantics:
   - Returns direct reference to internal list (not copy)
   - Caller can modify returned list - intentional?
   - Should return copy for immutability? (defensive programming)
2. Performance:
   - O(1) lookup is optimal
   - Caller still needs O(degree) to iterate
3. API design:
   - Returning list vs. iterator - trade-offs?
   - Iterator would be memory efficient
   - List allows random access, consistent with current design
4. Documentation:
   - Specify vertices in list are integers [0, V-1]
   - Order of adjacency list (insertion order)
   - Can caller assume list changes reflect graph changes?
5. Safety considerations:
   - Returning mutable reference could cause issues
   - Users might accidentally modify graph structure
   - Consider returning tuple or unmodifiable view
6. Usage pattern:
   - Frequently called in BFS/DFS algorithms
   - Performance critical path - O(1) is essential
```

## Function: `outdegree(self, v: int) -> int`

```
Review outdegree computation:
1. Correctness:
   - Returns len(_adj[v]) - number of outgoing edges
   - Includes self-loops in count
   - Counts duplicates (if v→w appears twice, counts as 2)
2. Performance:
   - len() on Python list is O(1) in current implementations
   - Could cache results, but too frequently updated
3. Alternative implementations:
   - Could track outdegree array like indegree
   - Trade: +O(V) space, -O(1) lookup time
   - Current approach: O(1) lookup after adjacency list construction
4. Consistency:
   - Parallel to indegree() - symmetric API
   - Both O(1) operations - good design
5. Edge cases:
   - Vertex with no outgoing edges: returns 0 (correct)
   - Self-loop counts as 1 outdegree (correct)
   - Multiple edges to same vertex each count separate (verify requirement)
```

## Function: `indegree(self, v: int) -> int`

```
Analyze indegree tracking:
1. Correctness:
   - Returns _indegree[v] maintained during add_edge()
   - Direct tracking more efficient than counting incoming edges
   - Updates happen atomically with edge addition
2. Performance:
   - O(1) indegree query
   - Alternative (compute on demand) would be O(V + E) inefficient
   - Current approach: O(V) space, O(1) query good trade-off
3. Consistency with add_edge():
   - Increment happens every time edge added
   - Verify no missing increments or double increments
   - Self-loops increment indegree (correct)
4. Edge cases:
   - Vertex with no incoming edges: returns 0 (correct)
   - Self-loop: both indegree and outdegree increment
5. Alternative designs:
   - Could compute indegree on demand (no extra space)
   - Would require scanning all vertices' adjacency lists
   - O(V + E) computation too expensive for frequent queries
6. Data structure validation:
   - Sum of all indegrees should equal E
   - Sum of all outdegrees should equal E
   - Useful invariant to verify correctness
```

## Integration & API Quality

```
Review Digraph API and design:
1. Public API completeness:
   - Supports: construction, edge addition, vertex/edge count, neighbors, degrees
   - Missing: edge removal, graph traversal, visualization
   - Is API sufficient for WordNet use case?
2. Method naming consistency:
   - V(), E(): single letter method names - unconventional, consider verbosity
   - add_edge(): clear verb/object naming - good
   - adj(), outdegree(), indegree(): inconsistent verb/noun styles
3. Error handling philosophy:
   - Validates vertices but not logical errors (like add duplicate edges)
   - Is this intentional or should defensive checks be added?
4. Encapsulation:
   - Private methods: _validate_vertex() properly marked
   - Direct list return from adj() breaks encapsulation
5. Performance characteristics:
   - All operations O(1) except iteration - good
   - Space complexity O(V + E) - optimal for adjacency list
6. Type safety:
   - Type hints present on all methods - excellent
   - Return types clearly specified - aids IDE support
7. Extensibility:
   - Could add reverse graph construction efficiently
   - Consider method composition patterns
```

## Edge Cases & Special Scenarios

```
Test coverage for critical edge cases:
1. Empty graphs:
   - V=0: should create valid empty graph
   - add_edge() on empty graph: should work for any valid edge
   - Query methods on empty graph: return empty/zero
2. Single vertex:
   - V=1: only vertex is 0
   - add_edge(0, 0): self-loop
   - Degrees: valid states
3. Self-loops:
   - add_edge(v, v): increments both indegree[v] and outdegree count
   - Should indegree == outdegree + self_loops for vertex v?
4. Duplicate edges:
   - add_edge(v, w) called twice: creates two entries in adjacency list
   - Correct behavior or should prevent duplicates?
   - Impact on indegree/outdegree counts
5. Dense graphs:
   - Complete digraph: V*(V-1) edges
   - Memory requirements for V=1000, V=10000
   - Adjacency list vs. matrix trade-offs
6. Large V values:
   - V=1,000,000: memory requirements
   - Validation performance
   - List allocation performance
```

## Performance & Optimization

```
Suggest performance improvements and optimizations:
1. Bottleneck analysis:
   - add_edge(): O(1) but append() has worst-case O(V) amortized
   - adj(): O(1) lookup but iteration is O(degree)
   - indegree/outdegree: O(1) optimal
2. Optimization opportunities:
   - Cache indegrees separately (trade: space for simplicity, already done)
   - Detect and handle duplicate edges efficiently
   - Use numpy/array module for large graphs
3. Memory optimization:
   - Current space: O(V + E) - optimal for adjacency list
   - Consider lazy indegree computation if rarely queried
4. Query optimization:
   - Batch operations: multi-vertex queries
   - Parallel graph construction for large files
5. Profiling recommendations:
   - Benchmark add_edge() performance with varying degrees
   - Memory profiling with different V sizes
   - Cache efficiency analysis
6. Alternative data structures:
   - Adjacency matrix for dense graphs
   - Edge set for checking edge existence
   - Trade-offs analysis: space vs. query time
```

## Testing & Validation

```
Design comprehensive test suite for digraph.py:
1. Basic operations:
   - Create digraph, add edges, query properties
   - Verify V(), E() counts are accurate
   - Check degrees (indegree, outdegree) match additions
2. Edge cases:
   - Empty graph (V=0)
   - Single vertex, single edge
   - Self-loops, duplicate edges
   - Maximum sized graphs
3. Validation tests:
   - Invalid vertex indices raise ValueError
   - Out-of-range values caught
   - Error messages helpful
4. Invariant checks:
   - Sum of indegrees == E
   - Sum of outdegrees == E
   - All vertices in [0, V-1]
5. API consistency:
   - adj() returns correct adjacency list
   - Degrees consistent after edge additions
   - Order preservation in adjacency lists
6. Performance tests:
   - Benchmark add_edge() with varying E
   - Query performance with dense graphs
   - Memory profiling with large V
```
