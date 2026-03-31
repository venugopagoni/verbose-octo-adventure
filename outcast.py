from wordnet import WordNet
from typing import List


class Outcast:
    def __init__(self, wordnet: WordNet):
        if wordnet is None:
            raise ValueError("WordNet cannot be None")
        self._wordnet = wordnet

    # -----------------------------
    # Find outcast noun
    # -----------------------------
    def outcast(self, nouns: List[str]) -> str:
        if nouns is None or len(nouns) == 0:
            raise ValueError("Nouns list cannot be empty")

        # Validate all nouns
        for noun in nouns:
            if noun is None or not self._wordnet.is_noun(noun):
                raise ValueError(f"Invalid WordNet noun: {noun}")

        max_distance = -1
        outcast_noun = None

        # O(n^2) comparison
        for nounA in nouns:
            total_distance = 0

            for nounB in nouns:
                if nounA != nounB:
                    total_distance += self._wordnet.distance(nounA, nounB)

            if total_distance > max_distance:
                max_distance = total_distance
                outcast_noun = nounA

        return outcast_noun