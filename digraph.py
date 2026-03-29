class Digraph:
    def __init__(self, V: int):
        if V < 0:
            raise ValueError("Number of vertices must be nonnegative")
        self._V = V
        self._E = 0
        self._adj = [[] for _ in range(V)]
        self._indegree = [0] * V

    def V(self) -> int:
        return self._V

    def E(self) -> int:
        return self._E

    def _validate_vertex(self, v: int):
        if v < 0 or v >= self._V:
            raise ValueError(f"vertex {v} is not between 0 and {self._V - 1}")

    def add_edge(self, v: int, w: int):
        self._validate_vertex(v)
        self._validate_vertex(w)
        self._adj[v].append(w)
        self._indegree[w] += 1
        self._E += 1

    def adj(self, v: int) -> list[int]:
        self._validate_vertex(v)
        return self._adj[v]

    def outdegree(self, v: int) -> int:
        self._validate_vertex(v)
        return len(self._adj[v])

    def indegree(self, v: int) -> int:
        self._validate_vertex(v)
        return self._indegree[v]
