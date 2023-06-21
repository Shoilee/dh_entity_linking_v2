import pandas
from deezy_match_data_construction import construct_deezymatch_data, generate_test_data
from DeezyMatch import train as dm_train
import os


def k_fold_validation(file="pm_data/ccrdfconst/wikidata_human_name.pkl", k=2):
    master_df = pandas.read_pickle(file) # load 6178 entities

    DataFrameDict = {i: pandas.DataFrame() for i in range(0,k)} # key = [0, 9], value dataframe chunks

    for i in range(k):
        DataFrameDict[i] = master_df[618*i:618*(i+1)]

    for i in range(k):
        train_sample = pandas.DataFrame()
        test_sample = DataFrameDict[i]
        for dict_index in range(0, k):
            if dict_index == i:
                continue
            train_sample = pandas.concat([train_sample, DataFrameDict[dict_index]], ignore_index=True)

        # GENERATE TRAINING DATA
        train_sample.to_pickle('k_fold_validation/training_sample.pkl')
        construct_deezymatch_data('k_fold_validation/training_sample.pkl',  directory="k_fold_validation/")

        # GENERATE TEST DATA
        test_sample.to_pickle('k_fold_validation/test_sample.pkl')
        generate_test_data('k_fold_validation/test_sample.pkl', directory='k_fold_validation/')

        # train a new model
        dm_train(input_file_path=os.path.join("inputs", "input_dfm.yaml"),
                 dataset_path=os.path.join("k_fold_validation", "name_pairs.txt"),
                 model_name="test001")

        pass

