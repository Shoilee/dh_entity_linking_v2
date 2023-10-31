import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas
import numpy as np
import multiprocessing as mp
from joblib import Parallel, delayed
from tqdm import tqdm


def find_match(data_tuple):
    df1, df2 = data_tuple
    # df2 = pandas.read_csv("ground_truth_temp_expertsname.tsv", sep="\t", index_col=0).iloc[:, 5:]
    result_table = pandas.DataFrame(columns=df1.columns.tolist() + df2.columns.tolist())
    for index_1, row_1 in tqdm(df1.iterrows()):
        for index_2, row_2 in df2.iterrows():
            if str(row_1['pref_label']) == str(row_2['FullName']):
                row = row_1.append(row_2)
                result_table = result_table.append(row, ignore_index=True)
    return result_table


def matchExactString(df1, df2):
    n_workers = int(mp.cpu_count()*2)
    print(f"{n_workers} workers are available")

    def serial_dataframe(df1=df1, df2=df2):
        result_table = pandas.DataFrame(columns=df1.columns.tolist() + df2.columns.tolist())
        for index_1, row_1 in tqdm(df1.iterrows()):
            for index_2, row_2 in df2.iterrows():
                if str(row_1['pref_label']) == str(row_2['FullName']):
                    # print(f"{row_1['pref_label']}, {row_2['FullName']} is a match!")
                    row = row_1.append(row_2)
                    result_table = result_table.append(row, ignore_index=True)
        return result_table

    def parallelize_dataframe(big_df, small_df, func, n_cores):
        df_split = np.array_split(big_df, n_cores)
        pool = mp.Pool(n_cores)
        const_data = [small_df for _ in range(n_cores)]
        df = pandas.concat(pool.map(func, zip(df_split, const_data)))
        pool.close()
        pool.join()
        return df

    result_table = parallelize_dataframe(df1, df2, find_match, n_workers)
    # result_table = serial_dataframe()
    return result_table.drop_duplicates()
