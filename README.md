# ENTITY LINKING ON HISTORICAL DATA

```
entity_linking
|   README.md
|   main.py
└───nmvwdatadump
|   |   data_dump.py
|   |   filter_wiki_human.py
└───naive
|   |   naive_string_matching.py
└───dezzymatch
|   └───data
|   └───inputs
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

## Task Description
Given two (or more) Knowledge Graph, the task is to find the corresponding links of two person instance from two different data sources that indicates the same real-world person. <br>

![task_description_image](resources/task_description.png)
[edit_image](https://app.diagrams.net/#G1ZMdnviCDEguLUWB5kzItnAMo7Y3TQBse)
## Experiment Look-up Table

| Experiment no. | Data1 | Data2 | Sample size | Algorithm1 | Algorithm2 | Evaluation | File | 
| ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | -----------| ----------- |
| exp100 | NMVW | Wikidata |  6178 | Naive | DeezyMatch | Based on Ground Truth | [File](exp100) | 
| exp200 | NMVW | Bronbeek | (num of NMVW) - (num of Bronbeek) | Naive | DeezyMatch |  Based human evaluation | [File](exp200) | 

## Evaluation 
Report on Recall, Precision and F-score [code](utils/calculate_result.py)