import pandas, numpy
from tqdm import tqdm


def matchLastName(df1=pandas.read_pickle("nmvw_data/ccrdfconst/person_names.pkl"), df2 = pandas.read_csv("/Users/sarah_shoilee/Desktop/Sarah/Bronbeek_Data/csv_dump/Constituents.csv")):
    """
    @param df1: accepts dataframe with column ['name_label']
    @param df2: accepts dataframe with column ['FirstName', 'LastName', 'FullName']
    @return: dataframe with two more column ['retrieved_results', 'match']
    """
    print(f"Shape of NMVW constinuent: {df1.shape}")
    listOfName = df1['name_label'].tolist()
    print(f"Shape of Bronbeek constinuent: {df2.shape}")

    match = ["NO" for i in range(len(df2.index))]
    match_results = []

    for i, row in tqdm(df2.iterrows()):
        row_match_results = list()
        for name in listOfName:
            if str(row['LastName']) == list(str(name).split(" "))[-1]:
                print(f"{row['LastName']}, {str(name)} is a match!")
                row_match_results.append(str(name))
                match[i] = "YES"

        match_results.append(row_match_results)

    temp_df = pandas.DataFrame({'RetrievedNames': match_results, 'MATCH':match})
    result_table = pandas.concat([df2, temp_df], axis=1)
    #print(result_table[['LastName', 'DisplayName', 'RetrievedNames', 'MATCH']])
    return result_table
