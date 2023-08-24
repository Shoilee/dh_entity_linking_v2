import pandas
from tqdm import tqdm


def match_with_abbreviation(df1, df2):
    """
        Matches two DataFrames based on abbreviated names.

        This function takes two DataFrames, df1 and df2, and performs a matching operation based on abbreviated names.
        It generates abbreviated versions of names in both DataFrames and then merges them using the 'Abbreviations' column.

        Args:
            df1 (pandas.DataFrame): The first DataFrame containing 'name_label' and other relevant columns.
            df2 (pandas.DataFrame): The second DataFrame containing 'FirstName', 'LastName', and other relevant columns.

        Returns:
            pandas.DataFrame: A merged DataFrame containing matched rows from df1 and df2, based on abbreviated names.

        The get_initials function extracts initials from a given name by splitting the name into components and taking
        the first character of each component followed by a period. If a name has an error during abbreviation, it
        prints the name along with the error message.

        The function abbreviates names in both DataFrames, adds the 'Abbreviations' column, and then merges the DataFrames
        based on these abbreviated names. The resulting DataFrame includes all columns from df1 and df2.

        Note: Commented-out sections with previous matching logic have been replaced with the pandas.merge approach for efficiency.

        Example:
        df1:
        +----+--------------+---------------+
        |    |  name_label |  ...          |
        +----+--------------+---------------+
        |  0 | John Doe     | ...           |
        |  1 | Jane Smith   | ...           |
        +----+--------------+---------------+

        df2:
        +----+------------+-----------+ ... |
        |    |  FirstName | LastName  | ... |
        +----+------------+-----------+ ... |
        |  0 | John       | Johnson   | ... |
        |  1 | Mary       | Smith     | ... |
        +----+------------+-----------+ ... |

        match_with_abbreviation(df1, df2) returns:
        +----+--------------+--------------+---------------+--------------+---------------+
        |    |  name_label | Abbreviations|  FirstName    | LastName     | RetrievedNames|
        +----+--------------+--------------+---------------+--------------+---------------+
        |  0 | John Doe     | J. Doe       | John          | Johnson      | [John Doe]    |
        |  1 | Jane Smith   | J. Smith     | Mary          | Smith        | []            |
        +----+--------------+--------------+---------------+--------------+---------------+
        """

    def get_initials(name):
        if len(name.split(" ")) < 1:
            print(name)
            return

        names = name.split(' ')
        try:
            return ' '.join([f"{n[0]}." for n in names])
        except Exception as e:
            print(f'{name} has {str(e)} error')

    abbreviation_list = list()
    for i, row in df1.iterrows():
        firstnames = get_initials(" ".join(str(row['name_label']).split(" ")[:-1]))
        if firstnames:
            initial_and_surname = firstnames + " " + str(row['name_label']).split(" ")[-1]
        else:
            initial_and_surname = str(row['name_label']).split(" ")[-1]
        # print(f"{str(row['name_label'])} --> {initial_and_surname}")
        abbreviation_list.append(initial_and_surname)

    temp_df = pandas.DataFrame({'Abbreviations': abbreviation_list})
    df1 = pandas.concat([df1, temp_df], axis=1)

    # print(df1[['name_label', 'Abbreviations']])

    # print("#######################################################################")

    abbreviation_list = list()
    for i, row in df2.iterrows():
        firstnames = get_initials(str(row['FirstName']))
        if firstnames :
            initial_and_surname = firstnames + " " + str(row['LastName'])
        else:
            initial_and_surname = row['LastName']
        # print(f"{str(row['FirstName'])} {str(row['LastName'])}--> {initial_and_surname}")
        abbreviation_list.append(initial_and_surname)

    temp_df = pandas.DataFrame({'Abbreviations': abbreviation_list})
    df2 = pandas.concat([df2, temp_df], axis=1)

    # print(df2[['FirstName', 'LastName', 'Abbreviations']])

    """
    match = ["NO" for i in range(len(df2.index))]
    match_results = []
    for i, row_df2 in tqdm(df2.iterrows()):
        row_match_results = list()
        for j, row_df1 in df1.iterrows():
            if str(row_df2['Abbreviations']) == str(row_df1['Abbreviations']):
                row_match_results.append(str(row_df1['name_label']))
                match[i] = "YES"
        match_results.append(row_match_results)

    temp_df = pandas.DataFrame({'RetrievedNames': match_results, 'MATCH': match})
    result_table = pandas.concat([df2, temp_df], axis=1)
    # print(result_table[['FirstName', 'LastName', 'RetrievedNames', 'MATCH']])
    """

    # result_table = df2.join(df1, lsuffix="_left", rsuffix="_right")
    result_table = pandas.merge(df1, df2, on='Abbreviations')
    return result_table

