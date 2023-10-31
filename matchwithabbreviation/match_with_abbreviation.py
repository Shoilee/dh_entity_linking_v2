import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas
import numpy as np
import multiprocessing as mp
from tqdm import tqdm


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


def get_abbreviation(fullname):
    # checking if fullname is nan
    if type(fullname) == float and np.isnan(fullname):
        return
    firstnames = get_initials(" ".join(str(fullname).split(" ")[:-1]))
    lastname = fullname.split(" ")[-1]
    if firstnames:
        initial_and_surname = firstnames + " " + lastname
    else:
        initial_and_surname = lastname
    return initial_and_surname


def match_with_abbreviation(df1, df2):
    """
        Matches two DataFrames based on abbreviated names.

        This function takes two DataFrames, df1 and df2, and performs a matching operation based on abbreviated names.
        It generates abbreviated versions of names in both DataFrames and then merges them using the 'Abbreviations' column.

        Args:
            df1 (pandas.DataFrame): The first DataFrame containing 'pref_label' and other relevant columns.
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
        |    |  pref_label |  ...          |
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
        |    |  pref_label | Abbreviations|  FirstName    | LastName     | RetrievedNames|
        +----+--------------+--------------+---------------+--------------+---------------+
        |  0 | John Doe     | J. Doe       | John          | Johnson      | [John Doe]    |
        |  1 | Jane Smith   | J. Smith     | Mary          | Smith        | []            |
        +----+--------------+--------------+---------------+--------------+---------------+
        """

    n_workers = int(mp.cpu_count() * 2)
    print(f"{n_workers} workers are available")
    pool = mp.Pool(n_workers)
    df1['Abbreviation'] = pool.map(get_abbreviation, df1['pref_label'])

    df2['Abbreviation'] = pool.map(get_abbreviation, df2['FullName'])

    # result_table = df2.join(df1, lsuffix="_left", rsuffix="_right")
    result_table = pandas.merge(df1, df2, on='Abbreviation')
    return result_table.drop_duplicates()

