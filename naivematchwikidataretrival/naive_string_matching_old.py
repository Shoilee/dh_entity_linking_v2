import pandas
import rdflib
import time
from tqdm import tqdm


def read_file(file):
    df = pandas.read_csv(file, sep="\t")
    return df


# TODO add more languages; consider the language spoken by dutch colony or just specify I did it for two language

def retrieve_uri_from_label(label):
    g = rdflib.Graph()

    # match with any language, now match only with dutch and english language

    wikidata_query = f"""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX wd: <http://www.wikidata.org/entity/>
        PREFIX wdt: <http://www.wikidata.org/prop/direct/>

        select * where {{ 
            SERVICE <https://query.wikidata.org/sparql> {{
                ?human wdt:P31 wd:Q5 .
                {{?human rdfs:label "{label.replace('"', '')}"@nl}}
                UNION
                {{?human rdfs:label "{label.replace('"', '')}"@en}}
            }}
        }}
        """
    # print(wikidata_query)

    return [constituent['human'] for constituent in g.query(wikidata_query)]


def run(source_file, destination_file):
    df = pandas.read_pickle(source_file)

    try:
        result_table = pandas.DataFrame(columns=['name_label', 'retrieved_uri'])
        result_list = []
        for label in tqdm(df['name_label']):
            retrieved_uri = retrieve_uri_from_label(str(label))
            result_list.append(retrieved_uri)
            # df2 = {'name': label, 'wiki_uri': run_query(str(label))}
            temp_df = pandas.DataFrame([[label, retrieved_uri]], columns=['name_label', 'retrieved_uri'])
            result_table = pandas.concat([result_table, temp_df], ignore_index=True)
            time.sleep(1)

    finally:
        # append retrieved_uri to the dataframe
        temp_series = pandas.Series(result_list)
        df['retrieved_uri'] = temp_series.values
        df.to_pickle(destination_file)
