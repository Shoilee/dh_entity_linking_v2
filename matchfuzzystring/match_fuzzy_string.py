from thefuzz import fuzz
from thefuzz import process
import pandas
from tqdm import tqdm


def match_fuzzy_string(df1, df2, ratio=fuzz.partial_token_sort_ratio, max_score=75, candidate_size=3):
    # print(f"Shape of NMVW constinuent: {df1.shape}")
    # print(f"Shape of Bronbeek constinuent: {df2.shape}")

    list_of_names = [str(row['name_label']) for i,row in df1.iterrows()]

    match = ["NO" for i in range(len(df2.index))]
    match_results = []

    for i, row in tqdm(df2.iterrows()):
        row_match_results = list()
        row_match_results = process.extractBests(str(row['DisplayName']), list_of_names,
                                                 scorer=ratio, score_cutoff=max_score, limit=candidate_size)
        if len(row_match_results) > 0:
            match[i] = "YES"
        match_results.append(row_match_results)

    temp_df = pandas.DataFrame({'RetrievedNames': match_results, 'MATCH':match})
    result_table = pandas.concat([df2, temp_df], axis=1)
    print(result_table[['DisplayName', 'RetrievedNames', 'MATCH']].head(10))

    return result_table


