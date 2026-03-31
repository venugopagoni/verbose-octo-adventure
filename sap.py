from collections import deque
from typing import Iterable, Tuple, Union
from digraph import Digraph

class SAP:
    def __init__(self, G: Digraph):
        if G is None:
            raise ValueError("Digraph cannot be None")
        self._G = G

    def _bfs(self, sources: Union[int, Iterable[int]]) -> dict[int, int]:
        dist_to = {}
        queue = deque()
        
        if isinstance(sources, int):
            sources = [sources]
        
        sources = list(sources)
        self._validate_iterable(sources)

        for s in sources:
            dist_to[s] = 0
            queue.append(s)
                
        while queue:
            current = queue.popleft()
            for neighbor in self._G.adj(current):
                if neighbor not in dist_to:
                    dist_to[neighbor] = dist_to[current] + 1
                    queue.append(neighbor)
                    
        return dist_to

    def _compute_shortest_ancestral_path(self, dist_to_v: dict[int, int], dist_to_w: dict[int, int]) -> Tuple[int, int]:
        min_length = float('inf')
        ancestor = -1
        
        for node in dist_to_v:
            if node in dist_to_w:
                total_dist = dist_to_v[node] + dist_to_w[node]
                if total_dist < min_length:
                    min_length = total_dist
                    ancestor = node
                
        if ancestor == -1:
            return -1, -1
        return min_length, ancestor

    def _validate_vertex(self, v: int):
        if v < 0 or v >= self._G.V():
            raise ValueError(f"Vertex {v} is out of bounds")

    def _validate_iterable(self, vertices: Iterable[int]):
        if vertices is None:
            raise ValueError("Iterable cannot be None")
        for v in vertices:
            if v is None:
                raise ValueError("Vertex in iterable cannot be None")
            self._validate_vertex(v)

    def length(self, v: Union[int, Iterable[int]], w: Union[int, Iterable[int]]) -> int:
        dist_v = self._bfs(v)
        dist_w = self._bfs(w)
        length, _ = self._compute_shortest_ancestral_path(dist_v, dist_w)
        return length

    def ancestor(self, v: Union[int, Iterable[int]], w: Union[int, Iterable[int]]) -> int:
        dist_v = self._bfs(v)
        dist_w = self._bfs(w)
        _, ancestor = self._compute_shortest_ancestral_path(dist_v, dist_w)
        return ancestor