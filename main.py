import pandas

from nmvwdatadump.data_dump import run as dump, check_constituent, check_constituent_wikidata
from nmvwdatadump.filter_wiki_human import run as filter_wikidata, count_total_wikidata
from nmvwdatadump.get_person_name import merge_constituent, count_person, dump_name, construct_name_table, count_type
from nmvwdatadump.wikidata_dump import test_run
from nmvwdatadump.filter_object_by_constituent import run as filter_const
from utils.ttl_to_dataframe import run as ttl2dataframe
from deezy_match_data_construction import construct_deezymatch_data
from result import result
from naive_string_matching import run as naive_string_matching
from naive_string_matching_all import run as naive_string_matching_all
from data_count import text_file_count
from fuzzy_string_matching import run as fuzzy_string_matching
from k_fold_validation import k_fold_validation
from bronbeek_const_data_processing import FirstNameLastName, NaiveNMVWvsBronbeek, DeezyMatchNMVWvsBronbeek

if __name__ == '__main__':
    # make data_dump file, pass component for argument
    # Constituent end-point: "ccrdfconst", range: 75000 (last found 16700)
    # Object core end-point: ccrdf, range: 529407
    # Object with acquisition: ccrdfobjacquisition, range: 529407
    # Exhibition: ccrdfexh, range:1200 ; 301-400 did not work
    # Historical Events: "ccrdfhiseve", range: 70
    # Terms/thesaurus: "ccrdfthes", range:12000
    # dump("ccrdfconst", 58000, range=20)

    # check_constituent("ccrdfconst")
    # check_constituent_wikidata("ccrdfconst")

    # make a wikidata human filtering dump from all constituent
    # filter_wikidata(directory="data/test") # pass the FOLDER NAME containing ttl file
    # count_total_wikidata("data/ccrdfconst/const_wiki_filter_log.csv")

    # filter_person(directory="data/ccrdfconst") # pass the FOLDER NAME containing ttl file
    # dump_name('data/ccrdfconst_all.ttl')
    # count_person("data/const_person_filter_log.csv")
    # construct_name_table(directory="data/ccrdfconst/")
    # count_type(directory="data/ccrdfconst")

    # df = pandas.read_pickle("data/ccrdfconst/person_names.pkl")
    # print(df.shape)

    # test_run()

    # filter_const()

    # TODO: check why I took "data/ccrdfconst/wikidata_ccrdfconstQ5_full.ttl" and not 'data/ccrdfconst_all.ttl'; which one is the correct one
    # ttl2dataframe("data/ccrdfconst/wikidata_ccrdfconstQ5_full.ttl", "data/ccrdfconst/wikidata_human_name.pkl" )

    # Conducted on 3rd February
    # naive_string_matching("data/ccrdfconst/wikidata_human_name.pkl", "results/naive_string_matching_10.pkl")
    # naive_string_matching("/Users/sarah_shoilee/PycharmProjects/DeezyMatch4Const/ranker_results/test_candidates_deezymatch.pkl","results/naive_string_matching.pkl")
    # naive_string_matching_all('data/ccrdfconst/person_names.pkl', 'results/naive_string_matching_all.pkl')

    # df = pandas.read_pickle('results/naive_string_matching_all.pkl')
    # print(df[df['retrieved_uri'].apply(lambda x: len(x)) > 0])

    # generating precision and recall
    # result("results/naive_string_matching_618.pkl")

    # DEEZYMATCH
    # construct_deezymatch_data('data/ccrdfconst/wikidata_human_name.pkl', 'data/ccrdfconst/dataset-string-matching_all.pkl')

    #df = pandas.read_pickle("data/ccrdfconst/dataset-string-matching_finetune.pkl")

    #print(df.head())

    #text_file_count()

    # fuzzy_string_matching("/Users/sarah_shoilee/PycharmProjects/DeezyMatch4Const/ranker_results/test_faiss_3_candidates_deezymatch.pkl", 'results/test_faiss_3_candidates_deezymatch.pkl')
    # result("results/test_faiss_3_candidates_deezymatch.pkl")

    # k_fold_validation()

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

    pass


