# ENTITY LINKING ON HISTORICAL DATA

```
entity_linking
|   README.md
|   main.py
|   result.py
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
|   |   naive_string_matching.py
|   |   naive_string_matching_all.py
|   |   naive_string_matching_old.py
└───dezzymatch
|   |   preprocessingg.py
|   |   candidates
|   |   combined
|   |   deezy_match_data_construction.py
|   |   fuzzy_string_matching.py
|   |   models
|   |   queries
|   |   ranker_results
└───utils
|   |   utils.py
|   |   ttl_to_dataframe.py
└───exp100
|   └───k_fold_validation
|   |   |   candidates.txt
|   |   |   dataset-string-matching_all.txt
|   |   |   dataset-string-matching_train.txt
|   |   |   id_to_names.pickle
|   |   |   naive_string_matching.pkl
|   |   |   name_pairs.txt
|   |   |   name_to_id.pickle
|   |   |   queries.txt
|   |   |   randon_person_names_1236.pkl
|   |   |   result_faiss_3.pkl
|   |   |   result.pkl
|   |   |   resultDict_cosine_1.pickle
|   |   |   resultDict_cosine_3.pickle
|   |   |   resultDict_faiss_1.pickle
|   |   |   resultDict_faiss_3.pickle
|   |   |   test_sample.pkl
|   |   |   training_sample.pkl
|   |   k_fold_validation.ipynb
|   |   k_fold_validation.py
|   |   README.md
└───exp200
|   |   bronbeek_const_data_processing.py
|   |   bronbeekDeezyMatchExp.ipynb
```

## Experiment Look-up Table

| Experiment no. | Data1 | Data2 | Sample size | Algorithm1 | Algorithm2 | Evaluation | File | 
| ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | -----------| ----------- |
| exp100 | NMVW | Wikidata |  6178 | Naive | DeezyMatch | Based on Ground Truth | File | 
| exp200 | NMVW | Bronbeek | (num of NMVW) - (num of Bronbeek) | Naive | DeezyMatch |  Based human evaluation | File | 
