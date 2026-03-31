from digraph import Digraph
from sap import SAP
from typing import List, Iterable

class WordNet:
    def __init__(self, synsets: str, hypernyms: str):
        if synsets is None or hypernyms is None:
            raise ValueError("Filename cannot be None")
            
        self._noun_to_synset_ids = {}
        self._id_to_synset = {}
        
        vertices_count = self._read_synsets(synsets)
        G = self._read_hypernyms(hypernyms, vertices_count)
        
        if not self._is_rooted_dag(G):
            raise ValueError("The provided hypernyms do not form a rooted DAG")
            
        self._sap = SAP(G)

    def _read_synsets(self, filename: str) -> int:
        count = 0
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) < 2:
                    continue
                synset_id = int(parts[0])
                synset_str = parts[1]
                self._id_to_synset[synset_id] = synset_str
                
                for noun in synset_str.split():
                    if noun not in self._noun_to_synset_ids:
                        self._noun_to_synset_ids[noun] = []
                    self._noun_to_synset_ids[noun].append(synset_id)
                count += 1
        return count

    def _read_hypernyms(self, filename: str, V: int) -> Digraph:
        G = Digraph(V)
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split(',')
                if not parts:
                    continue
                synset_id = int(parts[0])
                for i in range(1, len(parts)):
                    hypernym_id = int(parts[i])
                    G.add_edge(synset_id, hypernym_id)
        return G

    def _is_rooted_dag(self, G: Digraph) -> bool:
        roots = 0
        for i in range(G.V()):
            if G.outdegree(i) == 0:
                roots += 1
        if roots != 1:
            return False
            
        visited = [False] * G.V()
        on_stack = [False] * G.V()
        
        for i in range(G.V()):
            if not visited[i]:
                if self._has_cycle(G, i, visited, on_stack):
                    return False
        return True

    def _has_cycle(self, G: Digraph, v: int, visited: List[bool], on_stack: List[bool]) -> bool:
        visited[v] = True
        on_stack[v] = True
        for w in G.adj(v):
            if not visited[w]:
                if self._has_cycle(G, w, visited, on_stack):
                    return True
            elif on_stack[w]:
                return True
        on_stack[v] = False
        return False

    def nouns(self) -> Iterable[str]:
        return self._noun_to_synset_ids.keys()

    def is_noun(self, word: str) -> bool:
        if word is None:
            raise ValueError("Word cannot be None")
        return word in self._noun_to_synset_ids

    def distance(self, nounA: str, nounB: str) -> int:
        if not self.is_noun(nounA) or not self.is_noun(nounB):
            raise ValueError("Not a WordNet noun")
        idsA = self._noun_to_synset_ids[nounA]
        idsB = self._noun_to_synset_ids[nounB]
        return self._sap.length(idsA, idsB)

    def sap(self, nounA: str, nounB: str) -> str:
        if not self.is_noun(nounA) or not self.is_noun(nounB):
            raise ValueError("Not a WordNet noun")
        idsA = self._noun_to_synset_ids[nounA]
        idsB = self._noun_to_synset_ids[nounB]
        ancestor_id = self._sap.ancestor(idsA, idsB)
        if ancestor_id == -1:
            raise ValueError("No common ancestor found")
        return self._id_to_synset[ancestor_id]

if __name__ == "__main__":
    pass
