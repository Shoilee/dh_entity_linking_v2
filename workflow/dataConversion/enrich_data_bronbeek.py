from rdflib import ConjunctiveGraph, URIRef, Graph, Namespace, Literal
from rdflib.namespace import SKOS, RDF, RDFS
from tqdm import tqdm

import os, sys, pandas

"""
Documentation for nquad parser: https://rdflib.readthedocs.io/en/stable/_modules/rdflib/plugins/parsers/nquads.html
Example: https://github.com/RDFLib/rdflib/blob/main/examples/conjunctive_graphs.py 
"""


def load_graph(directory):
    graphs = ConjunctiveGraph()

    # Loop through each NQ file
    for root, dirs, files in os.walk(directory):
        files = [f for f in files if f.endswith(".nq")]
        for file in files:
            try:
                graphs.parse(os.path.join(root, file), format="nquads")
            except UnicodeDecodeError:
                print(f"Error with: {os.path.join(root, file)}")
            print("\n======================\n")
            print(f"file: {os.path.join(root, file)}")
            print(f"Graph has "
                  f"{len([x for x in graphs.store.contexts()])} context/Named Graphs "
                  f"with {len(graphs.store)} triples")

    return graphs


def add_acquisition_event(directory, graphs):
    def run_query(graph):
        query = """
            PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

            SELECT ?event ?constituent ?object
            WHERE{
                ?conxrefdetailID <https://pressingmatter.nl/Bronbeek/ConXrefDetails/vocab/ConstituentID> ?constituent .
                ?conxrefdetailID <https://pressingmatter.nl/Bronbeek/ConXrefDetails/vocab/Prefix> ?event .
                ?conxrefdetailID <https://pressingmatter.nl/Bronbeek/ConXrefDetails/vocab/ConXrefID> ?conXref .
                ?conXref <https://pressingmatter.nl/Bronbeek/ConXrefs/vocab/ID> ?ID .
                ?conXref <https://pressingmatter.nl/Bronbeek/ConXrefs/vocab/TableID> ?TableID .
                FILTER (?TableID = "108"^^<https://pressingmatter.nl/Bronbeek/ConXrefs/interger>) .
                ?conXref <https://pressingmatter.nl/Bronbeek/ConXrefs/vocab/RoleTypeID> <https://pressingmatter.nl/Bronbeek/RoleTypes/2> .
                ?object <https://pressingmatter.nl/Bronbeek/Objects/vocab/ObjectID> ?ID .
            }
        """

        result = graph.query(query)

        rows = []
        for row in result:
            event, constituent, object = row
            rows.append({
                'event': str(event),
                'constituent': str(constituent),
                'object': str(object)
            })
        df = pandas.DataFrame(rows)

        return df

    def insert_links(df):
        crm = Namespace("http://www.cidoc-crm.org/cidoc-crm/")
        g = Graph()
        g.bind("crm", crm)

        try:
            for i, row in tqdm(df.iterrows()):
                event = str(row.iloc[0]).strip().replace('"', '')
                constituent = URIRef(str(row.iloc[1]).strip().replace('"', ''))
                object = URIRef(str(row.iloc[2]).strip().replace('"', ''))

                # print(f"event:{event}\n constituent:{constituent}\n object: {object}\n")

                prov_activity = URIRef("https://www.pressingmatter.nl/Bronbeek/Provenance/" + str(i + 1))
                acquisition = URIRef("https://www.pressingmatter.nl/Bronbeek/Acquisition/" + str(i + 1))

                g.add((prov_activity, RDF.type, crm.E7_Activity))
                g.add((prov_activity, crm.P14_carried_out_by, constituent))
                g.add((prov_activity, crm.P2_has_type, URIRef(u"http://vocab.getty.edu/aat/300055863")))
                g.add((prov_activity, crm.P9_consists_of, acquisition))
                g.add((acquisition, RDF.type, crm.E8_Acquisition))
                g.add((acquisition, crm.P23_transferred_title_from, constituent))
                g.add((acquisition, crm.P24_transferred_title_of, object))
                g.add((acquisition, RDFS.label, Literal(event)))

        finally:
            print(len(g))
            g.add((URIRef(u"http://vocab.getty.edu/aat/300055863"), RDF.type, crm.E55_Type))
            g.add((URIRef(u"http://vocab.getty.edu/aat/300055863"), RDFS.label, Literal("Provenance Activity")))
            return g

    insert_links(run_query(graphs))\
        .serialize(destination=os.path.join(directory, 'provenance_activity.ttl'))


def add_former_owner(directory, graphs):
    def run_query(graph):
        query = """
            PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

            SELECT ?event ?constituent ?object
            WHERE{
                ?conxrefdetailID <https://pressingmatter.nl/Bronbeek/ConXrefDetails/vocab/ConstituentID> ?constituent .
                ?conxrefdetailID <https://pressingmatter.nl/Bronbeek/ConXrefDetails/vocab/Prefix> ?event .
                ?conxrefdetailID <https://pressingmatter.nl/Bronbeek/ConXrefDetails/vocab/ConXrefID> ?conXref .
                ?conXref <https://pressingmatter.nl/Bronbeek/ConXrefs/vocab/ID> ?ID .
                ?conXref <https://pressingmatter.nl/Bronbeek/ConXrefs/vocab/TableID> ?TableID .
                FILTER (?TableID = "108"^^<https://pressingmatter.nl/Bronbeek/ConXrefs/interger>) .
                ?conXref <https://pressingmatter.nl/Bronbeek/ConXrefs/vocab/RoleTypeID> <https://pressingmatter.nl/Bronbeek/RoleTypes/5> .
                ?object <https://pressingmatter.nl/Bronbeek/Objects/vocab/ObjectID> ?ID .
            }
            }
        """

        result = graph.query(query)

        rows = []
        for row in result:
            event, constituent, object = row
            rows.append({
                'event': str(event),
                'constituent': str(constituent),
                'object': str(object)
            })
        df = pandas.DataFrame(rows)

        return df

    def insert_links(df):
        g = Graph()
        crm = Namespace("http://www.cidoc-crm.org/cidoc-crm/")
        g.bind("crm", crm)

        try:
            for i, row in tqdm(df.iterrows()):
                constituent = URIRef(str(row.iloc[1]).strip().replace('"', ''))
                object = URIRef(str(row.iloc[2]).strip().replace('"', ''))

                g.add((object, crm.P51_has_former_or_current_owner, constituent))
        finally:
            print(len(g))
            return g

    insert_links(run_query(graphs)) \
        .serialize(destination=os.path.join(directory, 'former_owner.ttl'))


def add_related_constituents(directory, graphs):
    def run_query(graph):
        query = """
                    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
                    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                    PREFIX owl: <http://www.w3.org/2002/07/owl#>
                    PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>

                    SELECT ?constituent ?object
                    WHERE{
                        ?conxrefdetailID <https://pressingmatter.nl/Bronbeek/ConXrefDetails/vocab/ConstituentID> ?constituent .
                        ?conxrefdetailID <https://pressingmatter.nl/Bronbeek/ConXrefDetails/vocab/RoleTypeID> ?RoleTypeID .
                        ?conxrefdetailID <https://pressingmatter.nl/Bronbeek/ConXrefDetails/vocab/ConXrefID> ?conxref .
                        ?conXref <https://pressingmatter.nl/Bronbeek/ConXrefs/vocab/ID> ?ID .
                        ?conXref <https://pressingmatter.nl/Bronbeek/ConXrefs/vocab/TableID> ?TableID .
                        FILTER (?TableID = "108"^^<https://pressingmatter.nl/Bronbeek/ConXrefs/interger>) .
                        ?conXref <https://pressingmatter.nl/Bronbeek/ConXrefs/vocab/RoleTypeID> <https://pressingmatter.nl/Bronbeek/RoleTypes/1> .
                        ?object <https://pressingmatter.nl/Bronbeek/Objects/vocab/ObjectID> ?ID .
                    }
                """

        result = graph.query(query)

        rows = []
        for row in result:
            constituent, object = row
            rows.append({
                'constituent': str(constituent),
                'object': str(object)
            })
        df = pandas.DataFrame(rows)

        return df

    def insert_links(df):
        g = Graph()
        crm = Namespace("http://www.cidoc-crm.org/cidoc-crm/")
        g.bind("crm", crm)

        try:
            for i, row in tqdm(df.iterrows()):
                constituent = URIRef(str(row.iloc[0]).strip().replace('"', ''))
                object = URIRef(str(row.iloc[1]).strip().replace('"', ''))

                g.add((object, SKOS.related, constituent))
        finally:
            print(len(g))
            return g

    insert_links(run_query(graphs)) \
        .serialize(destination=os.path.join(directory, 'person_related.ttl'))


def enrich_data(directory):
    all_graphs = load_graph(directory)
    print(len(all_graphs))

    add_acquisition_event(directory, all_graphs)
    add_former_owner(directory, all_graphs)
    add_related_constituents(directory, all_graphs)


if __name__ == "__main__":
    enrich_data(sys.argv[1])
