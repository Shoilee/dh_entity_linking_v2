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


def run(source_file, destination_file, directory='data/deezymatch/'):
    name_to_id = pandas.read_pickle(directory+'name_to_id.pickle')
    candidate_df = pandas.read_pickle(source_file, compression='infer')

    try:
        result_table = pandas.DataFrame(columns=['name_label', 'retrieved_uri'])
        truth_list = []
        for i, row in tqdm(candidate_df.iterrows()):
            retrieved_uri = []
            for candidate_label in row['cosine_dist'].keys():
                try:
                    retrieved_uri += retrieve_uri_from_label(str(candidate_label))
                except:
                    retrieved_uri += []
            retrieved_uri = list(set(retrieved_uri))

            try:
                truth_list.append(name_to_id[row['query']][0])
            except KeyError:
                truth_list.append('')
            # df2 = {'name': label, 'wiki_uri': run_query(str(label))}
            temp_df = pandas.DataFrame([[row['query'], retrieved_uri]], columns=['name_label', 'retrieved_uri'])
            result_table = pandas.concat([result_table, temp_df], ignore_index=True)
            time.sleep(.5)

    finally:
        # append truth_uri to the dataframe
        temp_series = pandas.Series(truth_list)
        result_table['wiki_uri'] = temp_series
        result_table.to_pickle(destination_file)
