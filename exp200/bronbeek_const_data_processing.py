import random

import pandas, math


def FirstNameLastName(file="/Users/sarah_shoilee/Desktop/Sarah/Bronbeek_Data/csv_dump/Constituents.csv"):
    """
    contact first name and last
    @rtype: .csv file
    @return: .csv file
    """

    df = pandas.read_csv(file)
    df['FullName'] = df['FirstName'] +" "+ df['LastName']

    df.to_csv(file, encoding='utf-8')


def NaiveNMVWvsBronbeek(data1="pm_data/ccrdfconst/person_names.pkl", data2="/Users/sarah_shoilee/Desktop/Sarah/Bronbeek_Data/csv_dump/Constituents.csv"):
    """
    take two csv file and find exact match in constituent names
    @param data1: pkl file
    @param data2: csv file
    @return:
    """

    df1 = pandas.read_pickle(data1)
    print(f"Shape of NMVW constinuent: {df1.shape}")
    # print(type(df1['name_label']))
    listA = df1['name_label'].tolist()

    df2 = pandas.read_csv(data2)
    print(f"Shape of Bronbeek constinuent: {df2.shape}")
    # print(type(df2['FullName']))
    listB = df2['FullName'].tolist()

    df3 = set(listA).intersection(listB)

    print(len(df3))

    for i in df2['FullName'][:10]:
        if i in df1['name_label']:
            print(f"{i} matches")
        print(f"Bronbeek name: {i}, random NMVW name: {df1['name_label'][random.randint(0, 30000)]}")

    # TODO implement result section with calculating p, r and f-score


def DeezyMatchNMVWvsBronbeek(data1="pm_data/ccrdfconst/person_names.pkl", data2="/Users/sarah_shoilee/Desktop/Sarah/Bronbeek_Data/csv_dump/Constituents.csv"):
    def PrepareData(data1, data2):
        """
        store query and candidate in a txt file in folder "/bronbeek"
        """
        # write candidate(NMVW const) in a text file
        df1 = pandas.read_pickle(data1)
        print(f"Shape of NMVW constinuent: {df1.shape}")
        df1['name_label'].to_csv('bronbeek/candidates.txt', sep=' ', index=False)

        # write query(bronbeek const) in a text file
        df2 = pandas.read_csv(data2)
        print(f"Shape of Bronbeek constinuent: {df2.shape}")
        df2['FullName'].to_csv('bronbeek/queries.txt', sep=' ', index=False)

    df = pandas.read_pickle("/Users/sarah_shoilee/PycharmProjects/entity_linking/ranker_results/exp200_candidates_deezymatch.pkl")

    df_filtered = df[df['candidate_original_ids'] == {}]

    PrepareData(data1, data2)
    print(len(df_filtered))
    print(df['candidate_original_ids'].values)
