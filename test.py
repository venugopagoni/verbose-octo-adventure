from wordnet import WordNet
from outcast import Outcast

def main():
    print("Loading WordNet Lexicon from mock text files...")

    synsets_path = "synsets.txt"
    hypernyms_path = sys.argv[2]
    
    wordnet = WordNet(synsets_path, hypernyms_path)
    print("WordNet loaded successfully!\n")

    nouns = list(wordnet.nouns())
    print("All nouns:", nouns)

    print("\nTotal nouns:", len(nouns))
    
    noun_a = "machine"
    noun_b = "device"

    print(f"\nDistance between '{noun_a}' and '{noun_b}': {wordnet.distance(noun_a, noun_b)}")

    print(f"SAP (common ancestor) between '{noun_a}' and '{noun_b}': {wordnet.sap(noun_a, noun_b)}")
    
    noun_c = "object"
    noun_d = "machine"

    print(f"\nDistance between '{noun_c}' and '{noun_d}': {wordnet.distance(noun_c, noun_d)}")
    print(f"SAP between '{noun_c}' and '{noun_d}': {wordnet.sap(noun_c, noun_d)}")

    outcast = Outcast(wordnet)
    test_nouns = ["entity", "object", "machine"]
    print("\nTesting Outcast with array:", test_nouns)
    print("Outcast is:", outcast.outcast(nouns))

if __name__ == "__main__":
    main()
