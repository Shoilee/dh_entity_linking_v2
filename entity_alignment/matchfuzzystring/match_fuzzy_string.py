import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=UserWarning)

import pandas
import numpy as np
import multiprocessing as mp
from tqdm import tqdm

from thefuzz import fuzz
from thefuzz import process


def find_match(data_tuple):
    df1, df2 = data_tuple

    df1['score'] = np.nan
    result_table = pandas.DataFrame(columns=df1.columns.tolist() + df2.columns.tolist())

    for index_1, row_1 in tqdm(df1.iterrows()):
        for index_2, row_2 in df2.iterrows():
            score = fuzz.partial_token_sort_ratio(str(row_1['pref_label']), str(row_2['LastName']))
            # print(f"{}, {}: {score}")
            # filter out names that have 4 or less character in it and score
            if score > 70 and len(str(row_1['pref_label'])) > 4:
                row_1['score'] = score
                row = row_1.append(row_2)
                result_table = result_table.append(row, ignore_index=True)

    return result_table


def match_fuzzy_string(df1, df2, ratio=fuzz.partial_token_sort_ratio, max_score=75, candidate_size=3):
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


