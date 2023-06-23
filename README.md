# ENTITY LINKING ON HISTORICAL DATA

```
entity_linking
|   README.md
|   main.py
└───nmvwdatadump: NMVW DATA PROCESSING
|   |   data_dump.py
|   |   filter_wiki_human.py
└───naive: WIKIDATA IDENTIFIER RETRIVAL USING NAIVE(EXACT) STRING MATCHING GIVEN INDIVIDUAL'S NAME
|   |   naive_string_matching.py
|   |   ~~naive_string_matching_all.py~~
|   |   ~~naive_string_matching_old.py~~
└───dezzymatch: WIKIDATA IDENTIFIER RETRIVAL USING FUZZY STRING MATCHING GIVEN INDIVIDUAL'S NAME
|   └───ranker_results
|   └───candidates
|   └───combined
|   └───data
|   └───inputs
|   └───models
|   └───queries
|   |   deezy_match_data_construction.py
|   |   fuzzy_string_matching.py
|   |   line_count_text_file.py
|   |   deezymatch.ipynb
└───utils
|   |   utils.py
|   |   result.py
└───exp100
|   └───data
|   └───results
|   └───k_fold_validation
|   |   construct_ground_truth.py
|   |   exp100.ipynb
|   |   README.md
└───exp200
|   └───data
|   └───results
|   |   README.md
|   |   bronbeek_const_data_processing.py
|   |   bronbeekDeezyMatchExp.ipynb
```

## Experiment Look-up Table

| Experiment no. | Data1 | Data2 | Sample size | Algorithm1 | Algorithm2 | Evaluation | File | 
| ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | -----------| ----------- |
| exp100 | NMVW | Wikidata |  6178 | Naive | DeezyMatch | Based on Ground Truth | [File](exp100) | 
| exp200 | NMVW | Bronbeek | (num of NMVW) - (num of Bronbeek) | Naive | DeezyMatch |  Based human evaluation | [File](exp200) | 
