import pandas

from data_dump import run as dump, check_constituent, check_constituent_wikidata
from filter_wiki_human import run as filter_wikidata, count_total_wikidata
from wikidata_dump import test_run
from filter_object_by_constituent import run as filter_const
from ttl_to_dataframe import run as ttl2dataframe
from deezy_match_data_construction import construct_deezymatch_data
from result import result
from naive_string_matching import run as naive_string_matching
from data_count import text_file_count
from fuzzy_string_matching import run as fuzzy_string_matching

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

    # test_run()

    # filter_const()

    # ttl2dataframe("data/ccrdfconst/wikidata_ccrdfconstQ5_full.ttl", "data/ccrdfconst/wikidata_human_name.pkl" )

    # Conducted on 3rd February
    # naive_string_matching("data/ccrdfconst/wikidata_human_name.pkl", "results/naive_string_matching_10.pkl")
    # naive_string_matching("/Users/sarah_shoilee/PycharmProjects/DeezyMatch4Const/ranker_results/test_candidates_deezymatch.pkl","results/naive_string_matching.pkl")

    # generating precision and recall
    # result("results/naive_string_matching_618.pkl")

    # DEEZYMATCH
    # construct_deezymatch_data('data/ccrdfconst/wikidata_human_name.pkl', 'data/ccrdfconst/dataset-string-matching_all.pkl')

    #df = pandas.read_pickle("data/ccrdfconst/dataset-string-matching_finetune.pkl")

    #print(df.head())

    #text_file_count()

    fuzzy_string_matching("/Users/sarah_shoilee/PycharmProjects/DeezyMatch4Const/ranker_results/test_faiss_3_candidates_deezymatch.pkl", 'results/test_faiss_3_candidates_deezymatch.pkl')
    result("results/test_faiss_3_candidates_deezymatch.pkl")

    pass


