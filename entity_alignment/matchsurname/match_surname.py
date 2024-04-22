import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas
import numpy as np
import multiprocessing as mp
from tqdm import tqdm


def find_match(data_tuple):
    df1, df2 = data_tuple
    result_table = pandas.DataFrame(columns=df1.columns.tolist() + df2.columns.tolist())

    for index_1, row_1 in tqdm(df1.iterrows()):
        for index_2, row_2 in df2.iterrows():
            if str(row_1['pref_label']).split(" ")[-1] == str(row_2['LastName']):
                row = row_1.append(row_2)
                result_table = result_table.append(row, ignore_index=True)

    return result_table


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

    n_workers = int(mp.cpu_count() * 2)
    print(f"{n_workers} workers are available")

    def parallelize_dataframe(big_df, small_df, func, n_cores):
        df_split = np.array_split(big_df, n_cores)
        pool = mp.Pool(n_cores)
        const_data = [small_df for _ in range(n_cores)]
        df = pandas.concat(pool.map(func, zip(df_split, const_data)))
        pool.close()
        pool.join()
        return df

    result_table = parallelize_dataframe(df1, df2, find_match, n_workers)
    return result_table.drop_duplicates()