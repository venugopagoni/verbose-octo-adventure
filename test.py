from wordnet import WordNet
from outcast import Outcast

def main():
    print("Loading WordNet Lexicon from mock text files...")
    wordnet = WordNet("synsets.txt", "hypernyms.txt")
    print("Successfully loaded WordNet!")
    
    print(f"Total nouns in our mini dictionary: {len(list(wordnet.nouns()))}")
    
    noun_a = "dog"
    noun_b = "cat"
    print(f"\nDistance between '{noun_a}' and '{noun_b}': {wordnet.distance(noun_a, noun_b)}")
    print(f"SAP (common ancestor) between '{noun_a}' and '{noun_b}': {wordnet.sap(noun_a, noun_b)}")
    
    noun_c = "dog"
    noun_d = "table"
    print(f"\nDistance between '{noun_c}' and '{noun_d}': {wordnet.distance(noun_c, noun_d)}")
    print(f"SAP between '{noun_c}' and '{noun_d}': {wordnet.sap(noun_c, noun_d)}")

    outcast = Outcast(wordnet)
    nouns = ["dog", "cat", "bird", "table"]
    print("\nTesting Outcast with array:", nouns)
    print("Outcast is:", outcast.outcast(nouns))

if __name__ == "__main__":
    main()
