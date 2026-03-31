import sys
from collections import deque
from typing import Iterable, Tuple, Union
from digraph import Digraph

class SAP:
    def __init__(self, G: Digraph):
        if G is None:
            raise ValueError("Digraph cannot be None")
        self._G = Digraph(G.V())
        for v in range(G.V()):
            for w in G.adj(v):
                self._G.add_edge(v, w)

    def _bfs(self, sources: Union[int, Iterable[int]]) -> dict[int, int]:
        dist_to = {}
        q = deque()
        
        if isinstance(sources, int):
            self._validate_vertex(sources)
            dist_to[sources] = 0
            q.append(sources)
        else:
            self._validate_iterable(sources)
            for v in sources:
                dist_to[v] = 0
                q.append(v)
                
        while q:
            current = q.popleft()
            for w in self._G.adj(current):
                if w not in dist_to:
                    dist_to[w] = dist_to[current] + 1
                    q.append(w)
                    
        return dist_to

    def _compute_shortest_ancestral_path(self, dist_to_v: dict[int, int], dist_to_w: dict[int, int]) -> Tuple[int, int]:
        min_length = float('inf')
        ancestor = -1
        
        common_ancestors = set(dist_to_v.keys()).intersection(set(dist_to_w.keys()))
        for a in common_ancestors:
            dist = dist_to_v[a] + dist_to_w[a]
            if dist < min_length:
                min_length = dist
                ancestor = a
                
        if ancestor == -1:
            return -1, -1
        return min_length, ancestor

    def _validate_vertex(self, v: int):
        if v < 0 or v >= self._G.V():
            raise ValueError(f"Vertex {v} is out of bounds")

    def _validate_iterable(self, v: Iterable[int]):
        if v is None:
            raise ValueError("Iterable cannot be None")
        count = 0
        for vertex in v:
            if vertex is None:
                raise ValueError("Vertex in iterable cannot be None")
            self._validate_vertex(vertex)
            count += 1

    def length(self, v: Union[int, Iterable[int]], w: Union[int, Iterable[int]]) -> int:
        dist_v = self._bfs(v)
        dist_w = self._bfs(w)
        length, _ = self._compute_shortest_ancestral_path(dist_v, dist_w)
        return length

    def ancestor(self, v: Union[int, Iterable[int]], w: Union[int, Iterable[int]]) -> int:
        dist_v = self._bfs(v)
        dist_w = self._bfs(w)
        _, anc = self._compute_shortest_ancestral_path(dist_v, dist_w)
        return anc

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python sap.py <digraph_file.txt>")
        sys.exit(1)
    
    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        # Simple file reader for digraphs
        lines = f.read().split()
    
    if not lines:
        sys.exit(0)
        
    V = int(lines[0])
    E = int(lines[1])
    G = Digraph(V)
    
    idx = 2
    for _ in range(E):
        if idx + 1 < len(lines):
            v, w = int(lines[idx]), int(lines[idx+1])
            G.add_edge(v, w)
            idx += 2
            
    sap = SAP(G)
    while True:
        try:
            line = input().strip()
            if not line:
                break
            parts = line.split()
            if len(parts) >= 2:
                v, w = int(parts[0]), int(parts[1])
                length = sap.length(v, w)
                ancestor = sap.ancestor(v, w)
                print(f"length = {length}, ancestor = {ancestor}")
        except EOFError:
            break
