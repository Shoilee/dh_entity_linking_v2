"""
    FILTER CONSTITUENT WITH WIKIDATA IDENTIFIER AND INSTANCE OF PERSON
"""
import pandas
import rdflib
import glob, os, time


# Load data in a graph and run the query and add them to the new graph
def run_query(file, new_graph):
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
        ?s a crm:E21_Person.
         ?s ?prop ?val ;
             (a|!a)+ ?child . 
         ?child ?childProp ?childPropVal.
         ?someSubj ?incomingChildProp ?child. 
         FILTER(?child != <http://vocab.getty.edu/aat/300404670>).
    }
    """

    # print(len(g.query(q)))

    for row in g.query(q):
        temp_graph.add(row)
        new_graph.add(row)

    return len(g), len(g.query(q1)), len(g.query(q)), len(temp_graph.query(q1))


def run(directory):
    new_graph = rdflib.Graph()
    log_table = pandas.DataFrame(columns=["const_range", "g_stmt_len", "const_len", "wiki_stmt_len", "wiki_len"])

    try:
        for subdir, dirs, files in os.walk(directory):
            files = [f for f in files if f.endswith(".ttl")]
            for file in sorted(files, key=lambda s: int(s.split("-")[-1].split(".")[-2])):
                if file is None:
                    continue
                # for file in glob.glob(f"{directory}/*.ttl"):
                start_time = time.time()
                g_stmt_len, const_len, wiki_stmt_len, wiki_len = run_query(directory+"/"+file, new_graph)
                print(f"file: {file.split('/')[-1]}, runtime: {round((time.time() - start_time), 4)}")
                temp_df = pandas.DataFrame([[file, g_stmt_len, const_len, wiki_stmt_len, wiki_len]], columns=["const_range", "g_stmt_len", "const_len", "wiki_stmt_len", "wiki_len"])
                log_table = pandas.concat([log_table, temp_df], ignore_index=True)
                # time.sleep(60)
    finally:
        # store the newly constructed graph in one file
        new_graph.serialize(destination=os.path.join(directory, "..", "wikidata_ccrdfconstQ5_full.ttl"))
        # show dataframe
        print(log_table.to_string())
        log_table.to_csv(path_or_buf=os.path.join(directory, "..", "const_wiki_filter_log.csv"), sep=',')


def test_query(file="test/ccrdfconst_1-20.ttl"):
    new_graph = rdflib.Graph()
    run_query(file, new_graph)
    new_graph.serialize(destination="wikidata_ccrdfconst_test.ttl")
    # TODO define what to test
    assert len(new_graph) != 0


def count_total_wikidata(file):
    df = pandas.read_csv(file)
    print(f"Total wiki human instance found: {df['wiki_len'].sum()}")



