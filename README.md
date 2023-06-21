# ENTITY LINKING ON HISTORICAL DATA

```
entity_linking
|   README.md
└───datadump
|   |   data_count.py
|   |   data_dump.py
|   |   filter_object_by_constituent.py
|   |   filter_wiki_human_old.py
|   |   filter_wiki_human.py
|   |   get_person_name.py
|   |   wikidata_dump.py
└───naive
|   |   preprocessing.py
└───dezzymatch
|   |   preprocessingg.py
└───utils
|   |   utils.py
|   |   ttl_to_dataframe.py


## Experiment Look-up Table

| Experiment no. | Data1 | Data2 | Sample size | Algorithm1 | Algorithm2 | Evaluation | File | 
| ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | -----------| ----------- |
| exp100 | NMVW | Wikidata |  6178 | Naive | DeezyMatch | Based on Ground Truth | File | 
| exp200 | NMVW | Bronbeek | (num of NMVW) - (num of Bronbeek) | Naive | DeezyMatch |  Based human evaluation | File | 
