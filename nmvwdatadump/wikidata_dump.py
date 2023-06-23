import pandas
import rdflib
import os, time
import json
import requests


# Load data in a graph and run the query and add them to the new graph
def run_query(file, new_graph):
    def json_dump(wikidata_id):
        # https: // www.wikidata.org / wiki / Special: EntityData / Q18644475.json
        # wikidata_id = "https://www.wikidata.org/entity/Q4115175"

        # filter the Q-number
        # q_number = wikidata_id.split("/").strip()
        # construct the dump url
        # json_url = "https://www.wikidata.org/wiki/Special:EntityData/" + q_number +".json"
        # save the json file
        # response = requests.get(json_url)  # (your url)
        # data = response.json()
        # with open("wiki/" + q_number+'.json', 'w') as f:
        #    json.dump(data, f)

        pass

    temp_graph = rdflib.Graph()
    g = rdflib.Graph().parse(file)

    # when cannot read the ttl file
    if len(g) == 0:
        return

    q1 = """
        prefix crm: <http://www.cidoc-crm.org/cidoc-crm/> 

        SELECT DISTINCT ?s WHERE{
            ?s a crm:E21_Person .
        }
    """

    q2 = """
    PREFIX la: <https://linked.art/ns/terms/>

        SELECT DISTINCT ?wikidata WHERE{
            ?s la:equivalent ?wikidata. 
        }
    """

    q = """
    PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
    PREFIX la: <https://linked.art/ns/terms/>
    PREFIX wd: <http://www.wikidata.org/entity/>
    PREFIX wdt: <http://www.wikidata.org/prop/direct/>


    CONSTRUCT {
       ?s la:equivalent ?wikidata. 
       ?s ?prop ?val .
       ?child ?childProp ?childPropVal . 
       ?someSubj ?incomingChildProp ?child .
    }
    WHERE {
        ?s la:equivalent ?wikidata. 
        BIND(IRI(REPLACE(STR(?wikidata), "https","http")) AS ?new_wikidata).
         SERVICE <https://query.wikidata.org/sparql> {
              ?new_wikidata wdt:P31 wd:Q5 .
          }
         ?s ?prop ?val ;
             (a|!a)+ ?child . 
         ?child ?childProp ?childPropVal.
         ?someSubj ?incomingChildProp ?child. 
         FILTER(?child != <http://vocab.getty.edu/aat/300404670>).
    }
    """

    # TODO make a json dump
    # define json_dump():
    # print(len(g.query(q)))

    for row in g.query(q):
        temp_graph.add(row)
        new_graph.add(row)

    q2_result = temp_graph.query(q2)
    for row in q2_result:
        print(row['wikidata'])
        # json_dump(row)
    return len(g), len(g.query(q1)), len(g.query(q)), len(temp_graph.query(q1))


def test_run(file="/Users/sarah_shoilee/PycharmProjects/dh_entity_linking/data/test/ccrdfconst_1-10.ttl"):
    new_graph = rdflib.Graph()
    log_table = pandas.DataFrame(columns=["const_range", "g_stmt_len", "const_len", "wiki_stmt_len", "wiki_len"])

    g_stmt_len, const_len, wiki_stmt_len, wiki_len = run_query(file, new_graph)
    temp_df = pandas.DataFrame([[file, g_stmt_len, const_len, wiki_stmt_len, wiki_len]],
                               columns=["const_range", "g_stmt_len", "const_len", "wiki_stmt_len",
                                        "wiki_len"])
    log_table = pandas.concat([log_table, temp_df], ignore_index=True)
    print(log_table.to_string())


def run(directory):
    new_graph = rdflib.Graph()
    log_table = pandas.DataFrame(columns=["const_range", "g_stmt_len", "const_len", "wiki_stmt_len", "wiki_len"])

    try:
        for subdir, dirs, files in os.walk(directory):
            files = [f for f in files if f.endswith(".ttl")]
            for file in sorted(files, key=lambda s: int(s.split("-")[-1].split(".")[-2])):
                # TODO read the file
                start_time = time.time()
                g_stmt_len, const_len, wiki_stmt_len, wiki_len = run_query(directory + "/" + file, new_graph)
                print(f"file: {file.split('/')[-1]}, runtime: {round((time.time() - start_time), 4)}")
                temp_df = pandas.DataFrame([[file, g_stmt_len, const_len, wiki_stmt_len, wiki_len]],
                                           columns=["const_range", "g_stmt_len", "const_len", "wiki_stmt_len",
                                                    "wiki_len"])
                log_table = pandas.concat([log_table, temp_df], ignore_index=True)
                time.sleep(60)
    finally:
        # store the newly constructed graph in one file
        new_graph.serialize(destination=os.path.join(directory, "..", "wikidata_ccrdfconstQ5_100l.ttl"))
        # show dataframe
        print(log_table.to_string())
        log_table.to_csv(path_or_buf=os.path.join(directory, "..", "const_wiki_filter_log.csv"), sep=',')





