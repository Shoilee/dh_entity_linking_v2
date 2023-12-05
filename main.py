import pandas, pickle

from nmvwdatadump.data_dump import run as dump, count_all_constituents, count_all_constituent_with_wikidata
from nmvwdatadump.filter_wiki_human import run as filter_wikidata, count_total_wikidata
from nmvwdatadump.get_person_name import merge_constituent, count_person, dump_name, construct_name_table, count_type
from nmvwdatadump.wikidata_dump import test_run
from nmvwdatadump.filter_object_by_constituent import run as filter_const
from exp100.construct_ground_truth import run as constructgroundtruthfromwikidata
from deezymatch.deezy_match_data_construction import construct_deezymatch_data
from utils.calculate_result import result
from naivematchwikidataretrival.naive_string_matching import run as naive_string_matching
from naivematchwikidataretrival.naive_string_matching_all import run as naive_string_matching_all
from deezymatch.line_count_text_file import text_file_count
from deezymatch.fuzzy_string_matching import run as fuzzy_string_matching
from exp200.bronbeek_const_data_processing import FirstNameLastName, NaiveNMVWvsBronbeek, DeezyMatchNMVWvsBronbeek
from matchsurname.match_surname import matchLastName
from matchwithabbreviation.match_with_abbreviation import match_with_abbreviation
from matchfuzzystring.match_fuzzy_string import match_fuzzy_string
from nmvwdatadump.print_stat import print_stat
from exp202.calculate_result import calculate_result

if __name__ == '__main__':
    """CODE FOR NMVW DATA DUMP GIVEN HTTP URI"""
    # make data_dump file, pass component for argument
    # Constituent end-point: "ccrdfconst", range: 75000 (last found 16700)
    # Object core end-point: ccrdf, range: 529407
    # Object with acquisition: ccrdfobjacquisition, range: 529407
    # Exhibition: ccrdfexh, range:1200 ; 301-400 did not work
    # Historical Events: "ccrdfhiseve", range: 70
    # Terms/thesaurus: "ccrdfthes", range:12000
    # dump("ccrdfconst", 58000, range=20)

    # count_all_constituents("ccrdfconst") # 51909 @ 22 Jun, 2023 ; see ../nmvw_data/ccrdfconst/const_stat.csv
    # count_all_constituent_with_wikidata("ccrdfconst")
    # 6165 @ 22 Jun, 2023 ; see ../nmvw_data/ccrdfconst/const_wikidata_human_stat.csv

    # exp100
    # Building ground truth
    #   Step-1: Filter constituent with wikidata identifier (format: .ttl)
    #   Step-2: Extract all possible name label from wikidata (format: .pkl)

    # new(filtered and merged) graph destination=os.path.join(directory, "..", "wikidata_ccrdfconstQ5_full.ttl")
    # filter_wikidata(directory="nmvw_data/ccrdfconst") # pass the FOLDER NAME containing ttl file;
    # count_total_wikidata("nmvw_data/const_wiki_filter_log.csv") # 6165 @ 22 Jun, 2023

    # constructgroundtruthfromwikidata("exp100/data/wikidata_ccrdfconstQ5_full.ttl", "exp100/data/ground_truth.pkl")

    # df = pandas.read_pickle("exp100/data/wikidata_human_name.pkl")
    # print(df.head(10))

    # To get all the names of nmvw constituent

    """
    # filter_person(directory="data/ccrdfconst") # pass the FOLDER NAME containing ttl file
    # dump_name('data/ccrdfconst_all.ttl')
    # count_person("data/const_person_filter_log.csv")
    # construct_name_table(directory="data/ccrdfconst/")
    # count_type(directory="data/ccrdfconst")

    # df = pandas.read_pickle("data/ccrdfconst/person_names.pkl")
    # print(df.shape)

    # test_run()

    # filter_const()
    """

    # NAIVE STRING MATCH ON GROUND TRUTH DATA
    # naive_string_matching("exp100/data/ground_truth.pkl", "exp100/results/naive_string_matching.pkl")
    # naive_string_matching("/Users/sarah_shoilee/PycharmProjects/DeezyMatch4Const/ranker_results/test_candidates_deezymatch.pkl","results/naive_string_matching.pkl")
    # naive_string_matching_all('data/ccrdfconst/person_names.pkl', 'results/naive_string_matching_all.pkl')

    # df = pandas.read_pickle('results/naive_string_matching_all.pkl')
    # print(df[df['retrieved_uri'].apply(lambda x: len(x)) > 0])

    # generating p and r
    # result("exp100/results/naive_string_matching.pkl")

    # DEEZYMATCH
    # construct_deezymatch_data('exp100/data/ground_truth.pkl', 'exp100/data/dataset-string-matching_all.pkl') # TODO what 'exp100/data/dataset-string-matching_all.pkl' stores and why

    #TODO maybe we do not need the following three lines
    """
    #df = pandas.read_pickle("data/ccrdfconst/dataset-string-matching_finetune.pkl")
    #print(df.head())
    #text_file_count()
    """

    # fuzzy_string_matching("/Users/sarah_shoilee/PycharmProjects/DeezyMatch4Const/ranker_results/test_faiss_3_candidates_deezymatch.pkl", 'results/test_faiss_3_candidates_deezymatch.pkl')
    # result("results/test_faiss_3_candidates_deezymatch.pkl")

    # df = pandas.read_pickle("pm_data/ccrdfconst/wikidata_human_name.pkl")
    # df_random_1236 = df.sample(n=1236)
    # df_random_1236.to_pickle('k_fold_validation/randon_person_names_1236.pkl')
    # naive_string_matching_all('k_fold_validation/randon_person_names_1236.pkl', 'k_fold_validation/naive_string_matching.pkl')

    """
    
    df = pandas.read_pickle('k_fold_validation/randon_person_names_1236.pkl').reset_index()
    temp_series = df['wiki_uri']
    result_table = pandas.read_pickle("k_fold_validation/naive_string_matching.pkl")
    result_table['wiki_uri'] = df['wiki_uri']

    result_table.to_pickle("k_fold_validation/naive_string_matching.pkl")
    result("k_fold_validation/naive_string_matching.pkl")"""

    # FirstNameLastName()
    # NaiveNMVWvsBronbeek()
    # DeezyMatchNMVWvsBronbeek()

    # CODE FOR SURNAME MATCH
    # result = matchLastName(df1=pandas.read_pickle("nmvw_data/ccrdfconst/person_names.pkl"),
                           # df2=pandas.read_csv("/Users/sarah_shoilee/Desktop/Sarah/Bronbeek_Data/csv_dump/Constituents.csv"))

    # with open("results/bronbeekToNmvwSurnameMatchResults.pkl", "wb") as handle:
        # pickle.dump(result, handle, protocol=pickle.HIGHEST_PROTOCOL)

    # df = pandas.read_pickle("results/bronbeekToNmvwSurnameMatchResults.pkl")
    # print(len(df.loc[df["MATCH"] == "YES"]))

    """
    # CODE FOR MATCH WITH ABBREVIATION
    result = match_with_abbreviation(df1=pandas.read_pickle("nmvw_data/ccrdfconst/person_names.pkl"),
                            df2=pandas.read_csv("/Users/sarah_shoilee/Desktop/Sarah/Bronbeek_Data/csv_dump/Constituents.csv"))

    with open("results/bronbeekToNmvwAbbreviationMatchResults.pkl", "wb") as handle:
        pickle.dump(result, handle, protocol=pickle.HIGHEST_PROTOCOL)

    df = pandas.read_pickle("results/bronbeekToNmvwAbbreviationMatchResults.pkl")
    print(len(df.index))
    """

    """
    result = match_fuzzy_string(df1=pandas.read_pickle("nmvw_data/ccrdfconst/person_names.pkl"),
                                df2=pandas.read_csv("/Users/sarah_shoilee/Desktop/Sarah/Bronbeek_Data/csv_dump/Constituents.csv"))

    with open("results/bronbeekToNmvwFuzzyNameMatchResults.pkl", "wb") as handle:
        pickle.dump(result, handle, protocol=pickle.HIGHEST_PROTOCOL)

    df = pandas.read_pickle("results/bronbeekToNmvwFuzzyNameMatchResults.pkl")
    print(len(df.loc[df["MATCH"] == "YES"]))
    """

    # print(print_stat('nmvw_data/ccrdfconst', ["crm:E21_Person", "crm:E39_Actor", "crm:E74_Group" ]))

    pass


