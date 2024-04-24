import requests
from requests.structures import CaseInsensitiveDict


class EmptyGraphError(Exception):
    """raise when URL response returned no data"""
    pass


def query(graph):
    q = """
        prefix crm: <http://www.cidoc-crm.org/cidoc-crm/> 
        prefix la: <https://linked.art/ns/terms/> 
        prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> 

        SELECT DISTINCT ?s WHERE
        {
            ?s a crm:E21_Person.
            # return all objects

        }
        """
    print(f"Number of object {len(g.query(q))}")


def response_to_file(ttl_text, destination_file):
    """
    Receive http response turtle response and store it in file
    :param ttl_text: the response is expected in turtle format
    :param destination_file: location where the graph will be stored
    :return:
    """
    from rdflib import Graph
    g = Graph()
    g.parse(data=ttl_text, format='ttl')

    # Loop through each triple in the graph (subj, pred, obj)
    for subj, pred, obj in g:
        # Check if there is at least one triple in the Graph
        if (subj, pred, obj) not in g:
            return EmptyGraphError

    g.serialize(destination=destination_file)


# RDF / XML to Turtle conversion
def convert_xmlTottl(xml_text, destination_file):
    from rdflib import Graph
    """
    This function receive rdf/xml and save converted to ttl into the destination file.
    """
    g = Graph()
    g.parse(data=xml_text, format='rdf')

    # Loop through each triple in the graph (subj, pred, obj)
    for subj, pred, obj in g:
        # Check if there is at least one triple in the Graph
        if (subj, pred, obj) not in g:
            raise Exception("It better be!")

    g.serialize(destination=destination_file)


# Replace blank nodes
def replace_bnode(e, bnode_map, baseIRI):
    import uuid
    import rdflib
    """ Replace blank nodes by entities
    
    Needed for rdflib which provides imported blank nodes with random IDs,
    which creates mismatches between splits on the same nodes.
    """
    if isinstance(e, rdflib.term.BNode):
        if e in bnode_map.keys():
            return bnode_map[e]

        e_id =  baseIRI+ uuid.uuid4().hex
        e_new = rdflib.URIRef(e_id)

        bnode_map[e] = e_new

        return e_new

    return e


def replace_triples(file, baseIRI):
    from rdflib import Graph
    """
    Replace blank nodes URI in turtle file
    """
    g = Graph()
    g.parse(file)

    dic = {}
    for s,p, o in g:
        s_new = replace_bnode(s, dic, baseIRI)
        o_new = replace_bnode(o, dic, baseIRI)

        if(s!= s_new) or (o!=o_new):
            g.remove((s, p, o))
            g.add((s_new, p, o_new))

    g.serialize(destination=file)


# Get URL Response
def get_URL_response(URL):
    try:
        headers = CaseInsensitiveDict()
        headers["Accept"] = "text/turtle"
        r = requests.get(url=URL, headers=headers, timeout=60)
        return r
    except ConnectionError as e:
        print(f"{URL} cannot be found")
        return e
    except Exception as e:
        print(e)
        return e


def test_get_URL_response():
    # api-endpoint
    url = "https://linkedart.wereldculturen.nl/ccrdf/ccrdfconst.py?command=search&query=*=*&fields=*&range=1-20"

    assert get_URL_response(url).status_code == 200