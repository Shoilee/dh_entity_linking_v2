import pandas
from thefuzz import fuzz, process
from tqdm import tqdm


def exact_string_match(df, candidate_list):
    match = ["NO" for i in range(len(df.index))]
    match_results = []

    for i, row in df.iterrows():
        row_match_results = list()
        row_match_results = list(set([str(row['name_label'])]).intersection(set(candidate_list)))
        if len(row_match_results) > 0:
            match[i] = "YES"

        match_results.append(row_match_results)

    temp_df = pandas.DataFrame({'retrieved_names': match_results, 'match': match})
    result_table = pandas.concat([df, temp_df], axis=1)

    return result_table


def match_lastName(df, candidate_list):
    match = ["NO" for i in range(len(df.index))]
    match_results = []

    for i, row in df.iterrows():
        row_match_results = list()
        for name in candidate_list:
            if list(str(row['name_label']).split(" "))[-1] == list(str(name).split(" "))[-1]:
                row_match_results.append(str(name))
                match[i] = "YES"

        match_results.append(row_match_results)

    temp_df = pandas.DataFrame({'retrieved_names': match_results, 'match': match})
    result_table = pandas.concat([df, temp_df], axis=1)

    return result_table


def match_with_abbreviation(df, candidate_list):
    def get_initials(name):
        if len(name.split(" ")) < 1:
            print(name)
            return

        names = name.split(' ')
        try:
            return ' '.join([f"{n[0]}." for n in names])
        except Exception as e:
            # print(f'{name} has {str(e)} error')
            pass

    abbreviation_list = list()
    for i, row in df.iterrows():
        firstnames = get_initials(" ".join(str(row['name_label']).split(" ")[:-1]))
        if firstnames:
            initial_and_surname = firstnames + " " + str(row['name_label']).split(" ")[-1]
        else:
            initial_and_surname = str(row['name_label']).split(" ")[-1]
        # print(f"{str(row['name_label'])} --> {initial_and_surname}")
        abbreviation_list.append(initial_and_surname)

    temp_df = pandas.DataFrame({'abbreviations': abbreviation_list})
    df = pandas.concat([df, temp_df], axis=1)

    abbrv_candidate_dict = dict()
    for item in candidate_list:
        firstnames = get_initials(" ".join(str(item).split(" ")[:-1]))
        if firstnames:
            initial_and_surname = firstnames + " " + str(item).split(" ")[-1]
        else:
            initial_and_surname = str(item).split(" ")[-1]
        abbrv_candidate_dict[initial_and_surname] = item

    match = ["NO" for i in range(len(df.index))]
    match_results = []
    # matching
    for i, row in df.iterrows():
        row_match_results = list()
        row_match_results = list(set([str(row['abbreviations'])]).intersection(set(abbrv_candidate_dict.keys())))
        if len(row_match_results) > 0:
            match[i] = "YES"
            # print(len(row_match_results))
            match_results.append([abbrv_candidate_dict[row_match_results[0]]])
        else:
            match_results.append([])
            
    # print(f"len of match_results:{len(match_results)}\nlen of match:{len(match)}")


    temp_df = pandas.DataFrame({'retrieved_names': match_results, 'match': match})
    result_table = pandas.concat([df, temp_df], axis=1)

    return result_table


def match_fuzzy_string(df, candidate_list, ratio=fuzz.partial_token_sort_ratio, max_score=70, candidate_size=3):
    match = ["NO" for i in range(len(df.index))]
    match_results = []

    for i, row in tqdm(df.iterrows()):
        row_match_results = list()
        row_match_results = process.extractBests(str(row['name_label']), candidate_list,
                                                 scorer=ratio, score_cutoff=max_score, limit=candidate_size)
        if len(row_match_results) > 0:
            match[i] = "YES"
            row_match_results = [item[0] for item in row_match_results]
        match_results.append(row_match_results)

    temp_df = pandas.DataFrame({'retrieved_names': match_results, 'match':match})
    result_table = pandas.concat([df, temp_df], axis=1)

    return result_table

