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
        result_table = pandas.DataFrame(columns=['nmvw_uri', 'name_label', 'retrieved_uri'])

        for i, row in tqdm(df.iterrows()):
            retrieved_uri = retrieve_uri_from_label(str(row['name_label']))

            temp_df = pandas.DataFrame([[row['nmvw_uri'], row['name_label'], retrieved_uri]], columns=['nmvw_uri', 'name_label', 'retrieved_uri'])
            result_table = pandas.concat([result_table, temp_df], ignore_index=True)
            time.sleep(1)

    finally:
        result_table.to_pickle(destination_file)
