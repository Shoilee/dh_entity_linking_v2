import pandas, numpy
from tqdm import tqdm


def matchLastName(df1, df2):
    """
        Match last names from one DataFrame with last names from another DataFrame.

        This function takes two DataFrames as input and attempts to match last names
        from the first DataFrame (df1) with last names from the second DataFrame (df2).
        It compares each last name in df2 with the last names extracted from df1 and
        updates a match status for each row in df2.

        Args:
            df1 (pandas.DataFrame): The DataFrame containing a 'name_label' column
                with names to be matched against.
            df2 (pandas.DataFrame): The DataFrame containing a 'LastName' column
                to be matched with last names from df1.

        Returns:
            pandas.DataFrame:
                A new DataFrame containing the original data from df2 along with
                additional columns:
                - 'RetrievedNames': A list of matching names retrieved from df1.
                - 'MATCH': A match status indicating whether a match was found ('YES')
                  or not ('NO') for each row in df2.

        Note:
            - This function assumes that last names in df1 are stored in the 'name_label'
              column, and last names in df2 are stored in the 'LastName' column.
            - The matching process is based on comparing the last name of each row in df2
              with the last names extracted from df1 using space separation.
            - The 'tqdm' module is used to display a progress bar during iteration through df2.
        """

    # print(f"Shape of NMVW constinuent: {df1.shape}")
    # print(f"Shape of Bronbeek constinuent: {df2.shape}")

    listOfName = df1['name_label'].tolist()

    match = ["NO" for i in range(len(df2.index))]
    match_results = []

    for i, row in tqdm(df2.iterrows()):
        row_match_results = list()
        for name in listOfName:
            if str(row['LastName']) == list(str(name).split(" "))[-1]:
                # print(f"{row['LastName']}, {str(name)} is a match!")
                row_match_results.append(str(name))
                match[i] = "YES"

        match_results.append(row_match_results)

    temp_df = pandas.DataFrame({'RetrievedNames': match_results, 'MATCH':match})
    result_table = pandas.concat([df2, temp_df], axis=1)
    #print(result_table[['LastName', 'DisplayName', 'RetrievedNames', 'MATCH']])
    return result_table
