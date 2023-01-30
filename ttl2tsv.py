import rdflib
import pandas
import time
from tqdm import tqdm

""" ADJUST THE QUERY AS YOUR LIKING """

q = """
   prefix crm: <http://www.cidoc-crm.org/cidoc-crm/> 
   prefix la: <https://linked.art/ns/terms/> 
   prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
   PREFIX wd: <http://www.wikidata.org/entity/>
   PREFIX wdt: <http://www.wikidata.org/prop/direct/>

   SELECT DISTINCT ?s ?name ?wikidata WHERE
   {
       ?s la:equivalent ?wikidata.
       ?s ?p ?o.
       ?s crm:P1_is_identified_by ?bnode.
       ?bnode crm:P190_has_symbolic_content ?name.
   }
   """


def linkedDataToDataFrame(source_file, destination_file, query=q, column_list=[]):
    """
    :param
        accepts .ttl as source_file
    :return
        DataFrame df
        File save tsv destination_file

    """

    g = rdflib.Graph().parse(source_file)
    result = g.query(query)
    df = pandas.DataFrame(result, columns=column_list)
    df.to_csv(destination_file, sep="\t", columns=column_list)

    return df


def get_wikidata_labels(wiki_uri):
    # TODO read the .tsv file
    # TODO go over each row or wiki identifier
    # TODO retrieve the rdfs:label for that Q_id
    # TODO append to the rightmost columns of the dataframe
    # TODO store in the same .tsv

    def run_query(var):
        g = rdflib.Graph()

        # match with any language, now match only with dutch and english language

        wikidata_query = """
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX wd: <http://www.wikidata.org/entity/>
        PREFIX wdt: <http://www.wikidata.org/prop/direct/>

        select * where { 
            SERVICE <https://query.wikidata.org/sparql> {
                <"""+var+"""> rdfs:label ?name .
            }
        }
        """
        # print(wikidata_query)

        return [row['name'] for row in g.query(wikidata_query)]

    return run_query(wiki_uri)


def run(source_file, destination_file):
    if not source_file:
        raise Exception("No source file!")
    if not destination_file:
        raise Exception("No destination file!")

    query = q
    column_list = ['nmvw_uri', 'name_label', 'wiki_uri']

    linkedDataToDataFrame(source_file, destination_file, query, column_list)

    # read the .tsv file
    df = pandas.read_csv(destination_file, sep='\t')

    wiki_names = []
    # go over each wiki identifier
    for q_id in tqdm(df['wiki_uri']):
        # retrieve the rdfs:label
        wiki_names.append(get_wikidata_labels(q_id))
        time.sleep(1)

    # append wiki_labels to the dataframe
    s = pandas.Series(wiki_names)
    df['wiki_label'] = s.values
    df.to_csv(destination_file, sep="\t")

    # store in the same .tsv
    df.to_csv(destination_file, sep="\t")


