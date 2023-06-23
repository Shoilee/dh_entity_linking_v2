# ENTITY LINKING ON HISTORICAL DATA

```
entity_linking
|   README.md
|   main.py
|   result.py
└───nmvwdatadump
|   |   data_dump.py
|   |   ~~filter_object_by_constituent.py~~
|   |   ~~filter_wiki_human_old.py~~
|   |   filter_wiki_human.py
|   |   ~~get_person_name.py~~
|   |   ~~wikidata_dump.py~~
└───naive
|   |   naive_string_matching.py
|   |   ~~naive_string_matching_all.py~~
|   |   ~~naive_string_matching_old.py~~
└───dezzymatch
|   |   candidates
|   |   combined
|   |   deezy_match_data_construction.py
|   |   fuzzy_string_matching.py
|   |   models
|   |   queries
|   |   ranker_results
└───utils
|   |   utils.py
└───exp100
|   └───data
|   └───results
|   |   README.md
|   └───k_fold_validation
|   |   k_fold_validation.ipynb
|   |   k_fold_validation.py
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
| exp100 | NMVW | Wikidata |  6178 | Naive | DeezyMatch | Based on Ground Truth | ![File](exp100) | 
| exp200 | NMVW | Bronbeek | (num of NMVW) - (num of Bronbeek) | Naive | DeezyMatch |  Based human evaluation | ![File](exp200) | 
