import pandas
from tqdm import tqdm


def matchExactString(df1, df2):
    listOfName = df1['name_label'].tolist()

    match = ["NO" for i in range(len(df2.index))]
    match_results = []

    for i, row in tqdm(df2.iterrows()):
        row_match_results = list()
        for name in listOfName:
            if str(row['FullName']) == str(name).split(" "):
                print(f"{row['FullName']}, {str(name)} is a match!")
                row_match_results.append(str(name))
                match[i] = "YES"

        match_results.append(row_match_results)

    temp_df = pandas.DataFrame({'RetrievedNames': match_results, 'MATCH': match})
    result_table = pandas.concat([df2, temp_df], axis=1)
    # print(result_table[['LastName', 'DisplayName', 'RetrievedNames', 'MATCH']])
    return result_table