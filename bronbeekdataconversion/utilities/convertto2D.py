import pandas, os
import rdflib, tqdm


def construct_nmvw_2D_table(directory, file):
    nmvw_2D_table = pandas.DataFrame(
        columns=["nmvw_uri", "pref_label", "birth_begin_time", "birth_end_time", "death_begin_time", "death_end_time"])

    print("Hello")
    try:
        g = rdflib.Graph().parse(os.path.join(directory, file))

        if len(g) == 0:
            print("Error loading rdf file. The graph is empty")
            return nmvw_2D_table

        q = """
                                prefix crm: <http://www.cidoc-crm.org/cidoc-crm/> 

                                SELECT ?s ?name ?birth_begin_time ?birth_end_time ?death_begin_time ?death_end_time WHERE{
                                    ?s a crm:E21_Person .
                                    ?s crm:P1_is_identified_by ?name_bnode .
                                    ?name_bnode crm:P2_has_type <http://vocab.getty.edu/aat/300404670> .
                                    ?name_bnode crm:P190_has_symbolic_content ?name .
                                OPTIONAL{
                                    ?s crm:P98i_was_born ?birth_bNode .
                                    ?birth_bNode a crm:E67_Birth .
                                    ?birth_bNode crm:P4_has_time-span ?b_time.
                                    ?b_time a crm:E52_Time-Span .
                                    ?b_time crm:P82a_begin_of_the_begin ?birth_begin_time .
                                    ?b_time crm:P82b_end_of_the_end ?birth_end_time .
                                }
                                OPTIONAL{
                                    ?s crm:P100i_died_in ?death_bNode .
                                    ?death_bNode a crm:E69_Death .
                                    ?death_bNode crm:P4_has_time-span ?d_time.
                                    ?d_time a crm:E52_Time-Span .
                                    ?d_time crm:P82a_begin_of_the_begin ?death_begin_time .
                                    ?d_time crm:P82b_end_of_the_end ?death_end_time .
                                }
                                }
                            """

        print(type(g.query(q)))
        for row in tqdm(g.query(q)):
            temp_table = pandas.DataFrame([[row['s'], row['name'], row['birth_begin_time'],
                                            row['birth_end_time'], row['death_begin_time'],
                                            row['death_end_time']]],
                                          columns=["nmvw_uri", "pref_label", "birth_begin_time",
                                                   "birth_end_time", "death_begin_time", "death_end_time"])
            nmvw_2D_table = pandas.concat([nmvw_2D_table, temp_table], ignore_index=True)

        return nmvw_2D_table

    except:
        print("Something went wrong in RDF to dataframe conversion")
