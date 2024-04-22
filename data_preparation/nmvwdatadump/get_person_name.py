"""
    FILTER CONSTITUENT WITH WIKIDATA IDENTIFIER AND INSTANCE OF PERSON
"""
import pandas
import rdflib
import glob, os, time
from tqdm import tqdm


# Load data in a graph and run the query and add them to the new graph
def run_query(file, new_graph):
    g = rdflib.Graph().parse(file)

    # when cannot read the ttl file
    if len(g) == 0:
        return

    q = """
        SELECT * WHERE{
            ?s ?p ?o .
        }
    """

    for row in g.query(q):
        new_graph.add(row)

    return new_graph


def merge_constituent(directory):
    new_graph = rdflib.Graph()

    try:
        for subdir, dirs, files in os.walk(directory):
            files = [f for f in files if f.endswith(".ttl")]
            for file in tqdm(sorted(files, key=lambda s: int(s.split("-")[-1].split(".")[-2]))[:2617]):
                if file is None:
                    continue
                new_graph = run_query(directory + "/" + file, new_graph)

                if new_graph is None:
                    pass

    finally:
        # store the newly constructed graph in one file
        new_graph.serialize(destination=os.path.join(directory, "..", "ccrdfconst_all.ttl"))
        print(len(new_graph))


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


def construct_name_table(directory):
    name_table = pandas.DataFrame(columns=["nmvw_uri", "name_label"])

    try:
        for subdir, dirs, files in os.walk(directory):
            files = [f for f in files if f.endswith(".ttl")]
            for file in tqdm(sorted(files, key=lambda s: int(s.split("-")[-1].split(".")[-2]))):
                if file is None:
                    continue

                g = rdflib.Graph().parse(os.path.join(directory, file))

                if len(g) == 0:
                    continue

                q = """
                        prefix crm: <http://www.cidoc-crm.org/cidoc-crm/> 

                        SELECT ?s ?name WHERE{
                            ?s a crm:E21_Person .
                            ?s crm:P1_is_identified_by ?bnode .
                            ?bnode crm:P2_has_type <http://vocab.getty.edu/aat/300404670> .
                            ?bnode crm:P190_has_symbolic_content ?name .
                        }
                    """

                for row in g.query(q):
                    temp_table = pandas.DataFrame([[row['s'], row['name']]],
                                                  columns=["nmvw_uri", "name_label"])
                    name_table = pandas.concat([name_table, temp_table], ignore_index=True)

    finally:
        print(name_table.shape)
        name_table.to_pickle('data/ccrdfconst/person_names.pkl')


def test_query(file="test/ccrdfconst_1-20.ttl"):
    new_graph = rdflib.Graph()
    run_query(file, new_graph)
    new_graph.serialize(destination="wikidata_ccrdfconst_test.ttl")
    # TODO define what to test
    assert len(new_graph) != 0


def count_person(file):
    df = pandas.read_csv(file)
    print(f"Total human instance found: {df['person_len'].sum()}")


def dump_name(file):
    const_table = pandas.DataFrame(columns=["nmvw_uri", "name_label"])

    g = rdflib.Graph().parse(file)

    # when cannot read the ttl file
    if len(g) == 0:
        return

    q = """
            prefix crm: <http://www.cidoc-crm.org/cidoc-crm/> 

            SELECT ?s ?name WHERE{
                ?s a crm:E21_Person .
                ?s crm:P1_is_identified_by ?bnode .
                ?bnode crm:P2_has_type <http://vocab.getty.edu/aat/300404670> .
                ?bnode crm:P190_has_symbolic_content ?name .
            }
        """

    for row in g.query(q):
        temp_table = pandas.DataFrame([[row['s'], row['label']]],
                                                columns=["nmvw_uri", "name_label"])
        const_table = pandas.concat([const_table, temp_table], ignore_index=True)

    print(const_table.shape)
    # const_table.to_pickle('data/ccrdfconst/person_names.pkl')


def count_type(directory):
    count = 0
    try:
        for subdir, dirs, files in os.walk(directory):
            files = [f for f in files if f.endswith(".ttl")]
            for file in tqdm(sorted(files, key=lambda s: int(s.split("-")[-1].split(".")[-2]))):
                if file is None:
                    continue

                g = rdflib.Graph().parse(os.path.join(directory, file))

                if len(g) == 0:
                    continue

                q = """
                        prefix crm: <http://www.cidoc-crm.org/cidoc-crm/> 

                        SELECT (COUNT(DISTINCT ?s) AS ?n) WHERE{
                            ?s a crm:E39_Actor .
                        }
                    """

                for row in g.query(q):
                    count += int(row['n'])

    finally:
        print(count)