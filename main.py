from data_dump import run as dump, check_constituent, check_constituent_wikidata
from filter_wiki_human import run as filter_wikidata, count_total_wikidata
from wikidata_dump import test_run
from filter_object_by_constituent import run as filter_const
from ttl2tsv import run as ttl2tsv
from result import result
from naive_string_matching import run as naive_string_matching
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
    # filter_wikidata(directory="/Users/sarah_shoilee/PycharmProjects/dh_entity_linking/data/test") # pass the FOLDER NAME containing ttl file

    # count_total_wikidata("/Users/sarah_shoilee/PycharmProjects/dh_entity_linking/data/ccrdfconst/const_wiki_filter_log.csv")

    # test_run()

    # filter_const()

    # ttl2tsv("/Users/sarah_shoilee/PycharmProjects/dh_entity_linking/data/ccrdfconst/wikidata_ccrdfconstQ5_full.ttl", "/Users/sarah_shoilee/PycharmProjects/dh_entity_linking/data/ccrdfconst/wikidata_human_name.tsv" )

    # naive_string_matching("data/ccrdfconst/wikidata_human_name.tsv", "results/naive_string_matching.tsv")

    result("results/naive_string_matching.tsv")

