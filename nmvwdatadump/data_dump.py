import pandas
import rdflib
import requests
from utils.utils import EmptyGraphError
import os, logger
from utils.utils import get_URL_response, convert_xmlTottl, replace_triples, response_to_file

# TODO CHECK WHETHER IT PROPERLY DETECTS EMPTY RETURN


def test_url():
    # api-endpoint
    # url = "https://linkedart.wereldculturen.nl/ccrdf/ccrdfconst.py?command=search&query=*=*&fields=*&range=201-300"
    url = "https://linkedart.wereldculturen.nl/ccrdf/ccrdfobjacquisition.py?command=search&query=*=*&fields=*&range=221101-221200"

    # sending get request and saving the response as response object
    response = get_URL_response(url)
    print(response.text.__contains__("UnicodeDecodeError"))
    assert response.status_code == 200


def run(component, highest_value, range, start_limit=1):
    """
    Extract data from end-point
    :param start_limit: (int) default 1; indicate the starting range value for GET request
    :param component: (str) specify which component to access from end-point
    :param highest_value: (int) possible highest number for the component range
    :param range: (int) URL request range
    :return: store the downloaded file in desired directory
    """
    directory = "data/" + component
    print(directory)
    # make new directory for current component
    if not os.path.exists(directory):
        os.makedirs(directory)

    # loop to cover the entire data-range
    base_url = "https://linkedart.wereldculturen.nl/ccrdf"

    # start_limit = 16601
    end_limit = start_limit + range - 1

    while end_limit <= highest_value:
        destination_file = directory + "/" + component + "_" + str(start_limit) + "-" + str(end_limit) + ".ttl"
        url = base_url + "/" + component + ".py?command=search&query=*=*&fields=*&range=" + str(start_limit) + "-" + str(end_limit)
        baseIRI = "http://www.example.com/" + component + "/"

        print(url)

        try:
            response = get_URL_response(url)
        except Exception as e:
            print(e)
            print(url)
            start_limit = end_limit + 1
            end_limit = start_limit + range - 1
            continue

        # TODO handle Readtimeout error; Stops running when
        #  """AttributeError: 'ReadTimeout' object has no attribute 'text'
        #  HTTPSConnectionPool(host='linkedart.wereldculturen.nl', port=443): Read timed out. (read timeout=10)"""
        # TODO find a better way to handle such exception
        if not response.text.__contains__("UnicodeDecodeError") or not isinstance(response, Exception):
            try:
                # convert_xmlTottl(response.text, destination_file)
                # TODO it is supposed to throw EmptyGraphError if URL returns blank/empty response
                response_to_file(response.text, destination_file) # expect ttl response
                replace_triples(destination_file, baseIRI)
            except Exception as e:
                if type(e) == EmptyGraphError:
                    with open("data/" + component + "/empty_graph_error.txt", "a+") as f:
                        f.write(f"{url}\n")
                        f.write(f"{str(e)}\n")
                with open("data/" + component + "/conversion_error.txt", "a+") as f:
                    f.write(f"{url}\n")
                    f.write(f"{str(e)}\n")

        else:
            with open("data/"+component+"/check_error.txt", "a+") as f:
                f.write(f"range: {start_limit}-{end_limit}\n")

        start_limit = end_limit + 1
        end_limit = start_limit + range - 1
    return


def check_constituent(component):
    directory = "data/"+component

    def count_graph(file):
        g = rdflib.Graph().parse(file)

        # when cannot read the ttl file
        if len(g) == 0:
            return

        q = """
                prefix crm: <http://www.cidoc-crm.org/cidoc-crm/> 

                SELECT DISTINCT ?s WHERE{
                    ?s a ?type .
                    FILTER((?type = crm:E21_Person) || (?type = crm:E74_Group) || (?type = crm:E39_Actor)).
                }
            """
        return len(g), len(g.query(q))

    log_table = pandas.DataFrame(columns=["const_range", "g_stmt_len", "const_len"])

    try:
        for subdir, dirs, files in os.walk(directory):
            files = [f for f in files if f.endswith(".ttl")]
            for file in sorted(files, key=lambda s: int(s.split("-")[-1].split(".")[-2])):
                if os.stat(directory + "/" + file).st_size == 0:
                    continue
                if count_graph(directory + "/" + file) is None:
                    print("What the hell!")
                    continue
                g_stmt_len, const_len = count_graph(directory + "/" + file)
                temp_df = pandas.DataFrame([[file, g_stmt_len, const_len]],
                                           columns=["const_range", "g_stmt_len", "const_len"])
                log_table = pandas.concat([log_table, temp_df], ignore_index=True)
    finally:
        print(log_table.to_string())
        log_table.to_csv(path_or_buf=os.path.join(directory, "const_stat.csv"), sep=',')
        print(log_table['const_len'].sum())


def check_constituent_wikidata(component):
    directory = "data/"+component

    def count_graph(file):
        g = rdflib.Graph().parse(file)

        # when cannot read the ttl file
        if len(g) == 0:
            return

        q = """
                prefix crm: <http://www.cidoc-crm.org/cidoc-crm/> 
                PREFIX la: <https://linked.art/ns/terms/>

                SELECT DISTINCT ?s WHERE{
                    ?s a ?type .
                    ?s la:equivalent ?wikidata. 
                    FILTER((?type = crm:E21_Person)).
                }
            """
        return len(g), len(g.query(q))

    log_table = pandas.DataFrame(columns=["const_range", "g_stmt_len", "const_len"])

    try:
        for subdir, dirs, files in os.walk(directory):
            files = [f for f in files if f.endswith(".ttl")]
            for file in sorted(files, key=lambda s: int(s.split("-")[-1].split(".")[-2])):
                if os.stat(directory + "/" + file).st_size == 0:
                    continue
                if count_graph(directory + "/" + file) is None:
                    continue
                g_stmt_len, const_len = count_graph(directory + "/" + file)
                temp_df = pandas.DataFrame([[file, g_stmt_len, const_len]],
                                           columns=["const_range", "g_stmt_len", "const_len"])
                log_table = pandas.concat([log_table, temp_df], ignore_index=True)
    finally:
        # print(log_table.to_string())
        log_table.to_csv(path_or_buf=os.path.join(directory, "const_wikidata_human_stat.csv"), sep=',')
        print(log_table['const_len'].sum())