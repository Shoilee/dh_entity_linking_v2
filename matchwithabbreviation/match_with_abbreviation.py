import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas
import numpy as np
import multiprocessing as mp
from tqdm import tqdm
import re


def get_initials(name):
    """
        Extracts the initials from a given name or a name with specific patterns.

        Args:
        - name (str): A string containing the name to extract initials from.

        Returns:
        - str or None:
            - If the name follows a standard pattern (e.g., 'First Middle Last'), it returns the initials in the format 'F.M.L.'
            - If the name contains unusual patterns (e.g., initials already in the name or fullname enclosed in brackets),
            it removes brackets and returns the initials in the appropriate format.
            - If the initial is already there  it just returns the initial as it is.

        Note:
        - This function identifies and handles specific patterns within the name:
          1. Removes content enclosed within brackets.
          2. Processes initials separated by periods (e.g., 'J.D.' for 'John Doe').
          3. Extracts initials from a standard name format and concatenates them with periods ('John Adam Smith' -> 'J.A.S.').
          4. In case of any error during the process, it does not raise exceptions but remains silent.

        Examples:
        >>> get_initials("John Adam Smith")
        'J.A.S.'

        >>> get_initials("J.H. (James Henry)")
        'J.H.'

        >>> get_initials("A.B.C.")
        'A.B.C.'

        """

    # the pattern for brackets containing some content
    pattern = "\(.*?\)"
    if bool(re.search(pattern, name)):
        name = re.sub(pattern, "", name)
        return "".join(name.split(' ')[:-1])

    if len(name.split(" ")) < 1:
        return

    names = name.split(' ')
    if len(names) == 1 and bool(re.search("\.", "".join(names))):
        return "".join(names)
    else:
        try:
            return ''.join([f"{n[0]}." for n in names])
        except Exception as e:
            # print(f'{name} has {str(e)} error')
            pass


def get_abbreviation(fullname):
    # checking if fullname is nan
    if type(fullname) == float and np.isnan(fullname):
        return
    fullname = fullname.strip()
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
        |  1 | Jane       | Smith     | ... |
        +----+------------+-----------+ ... |

        match_with_abbreviation(df1, df2) returns:
        +----+--------------+--------------+---------------+--------------+
        |    |  pref_label | Abbreviations|  FirstName    | LastName     |
        +----+--------------+--------------+---------------+--------------+
        |  0 | John Doe     | J. Doe       | John          | Johnson      |
        |  1 | Jane Smith   | J. Smith     | Jane          | Smith        |
        +----+--------------+--------------+---------------+--------------+
        """

    n_workers = int(mp.cpu_count() * 2)
    print(f"{n_workers} workers are available")
    pool = mp.Pool(n_workers)
    df1['Abbreviation'] = pool.map(get_abbreviation, df1['pref_label'])
    df2['Abbreviation'] = pool.map(get_abbreviation, df2['FullName'])

    # result_table = df2.join(df1, lsuffix="_left", rsuffix="_right")
    result_table = pandas.merge(df1, df2, on='Abbreviation')
    return result_table.drop_duplicates()

