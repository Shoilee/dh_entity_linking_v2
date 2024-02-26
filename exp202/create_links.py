import os, pandas, sys
from rdflib import Graph, URIRef
from rdflib.namespace import OWL

def create_link_graph(df):
    g = Graph()

    for _ , row in df.iterrows():
        uri_nmvw = str(row['nmvw_uri'])
        constituent_id_bronbeek = str(int(row['ConstituentID']))
        uri_bronbeek = "https://pressingmatter.nl/Bronbeek/Constituents/" + constituent_id_bronbeek

        uri_nmvw = URIRef(uri_nmvw)
        uri_bronbeek = URIRef(uri_bronbeek)

        g.add((uri_nmvw, OWL.sameAs, uri_bronbeek))
    
    return g


if __name__ == "__main__":
    file_path = sys.argv[1]

    df = pandas.read_csv(file_path, sep='\t', index_col=0)
    create_link_graph(df).serialize(destination=os.path.join(os.path.dirname*(file_path), os.path.basename(file_path), '.ttl'))