import sys
from wordnet import WordNet
from typing import List

class Outcast:
    def __init__(self, wordnet: WordNet):
        if wordnet is None:
            raise ValueError("WordNet cannot be None")
        self._wordnet = wordnet

    def outcast(self, nouns: List[str]) -> str:
        if not nouns:
            raise ValueError("Nouns list cannot be empty or None")
            
        for noun in nouns:
            if noun is None or not self._wordnet.is_noun(noun):
                raise ValueError("List contains invalid WordNet nouns")
                
        outcast_noun = None
        max_dist = -1
        
        for i in range(len(nouns)):
            dist = 0
            for j in range(len(nouns)):
                if i != j:
                    dist += self._wordnet.distance(nouns[i], nouns[j])
            if dist > max_dist:
                max_dist = dist
                outcast_noun = nouns[i]
                
        return outcast_noun

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python outcast.py <synsets.txt> <hypernyms.txt> <outcast_files...>")
        sys.exit(1)
        
    synsets_file = sys.argv[1]
    hypernyms_file = sys.argv[2]
    
    wordnet = WordNet(synsets_file, hypernyms_file)
    outcast_finder = Outcast(wordnet)
    
    for i in range(3, len(sys.argv)):
        outcast_file = sys.argv[i]
        with open(outcast_file, 'r', encoding='utf-8') as f:
            nouns = f.read().split()
        print(f"{outcast_file}: {outcast_finder.outcast(nouns)}")
