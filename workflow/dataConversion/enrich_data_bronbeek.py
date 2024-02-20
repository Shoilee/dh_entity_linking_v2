from rdflib import ConjunctiveGraph, URIRef
from rdflib.plugins.stores.memory import Memory
import rdflib.plugins.parsers.nquads

import os, sys

"""
Documentation for nquad parser: https://rdflib.readthedocs.io/en/stable/_modules/rdflib/plugins/parsers/nquads.html
Example: https://github.com/RDFLib/rdflib/blob/main/examples/conjunctive_graphs.py 
"""


def load_graph(directory):
    store = Memory()
    graphs = ConjunctiveGraph(store=store)
    for root, dirs, files in os.walk(directory):
        for file in files:
            graphs = graphs.parse(os.path.join(root, file), format="nquads")
            print("\n======================\n")
            print(f"file: {os.path.join(root, file)}")
            print(f"Graph has "
                  f"{len([x for x in graphs.store.contexts()])} context/Named Graphs "
                  f"with {len(graphs.store)} triples")

    return graphs


def add_acquisition_event():
    def run_query(graph):
        # TODO: write query that will inject triples
        """
        @return: table or pandas dataframe
        """

        q = """
        SELECT * WHERE
        {
            ?s ?p ?o .
        } LIMIT 10
        """
    pass


def add_former_owner():
    def run_query(graph):
        # TODO: write query that will inject triples
        """
        @return: table or pandas dataframe
        """

        q = """
        SELECT * WHERE
        {
            ?s ?p ?o .
        } LIMIT 10
        """
    pass


def add_related_constituents():
    def run_query(graph):
        # TODO: write query that will inject triples
        """
        @return: table or pandas dataframe
        """

        q = """
        SELECT * WHERE
        {
            ?s ?p ?o .
        } LIMIT 10
        """
    pass


def enrich_data(directory):
    all_graphs = load_graph(directory)
    print(len(all_graphs.store))
    # run_query(all_graphs)


if __name__=="__main__":
    enrich_data(sys.argv[1])