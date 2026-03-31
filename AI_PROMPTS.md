# AI Prompts Log

## Problem 1: Missing runnable input path handling in test harness
- Exact prompt used:
  "Update test.py so that it locates WORDNET_LEXICON/synsets.txt and hypernyms.txt by default and supports command-line overrides, instead of hardcoding in current working directory."
- How output was modified:
  - Added command-line argument support
  - Added fallback to test directory's parent WORDNET_LEXICON path
  - Added FileNotFoundError with precise path reporting

## Problem 2: SAP iterable validation consuming generator
- Exact prompt used:
  "Fix SAP._bfs/_validate_iterable so generators can be passed without being consumed on validation."
- How output was modified:
  - Converted sources iterable to list in _bfs
  - _validate_iterable now checks elements without double-consumption

## Problem 3: WordNet.sap returned invalid ancestor id
- Exact prompt used:
  "Handle the case in WordNet.sap where ancestor id is -1 and no common ancestor exists."
- How output was modified:
  - Added explicit ValueError for ancestor_id == -1

## Problem 4: Add required rubric file AI_PROMPTS.md
- Exact prompt used:
  "Create AI_PROMPTS.md in repo root that meets the assignment standard: problem -> exact prompt -> output modification."
- How output was modified:
  - Added this file with entries for each AI-assisted fix.
