import rdflib, pandas, os


# Load data in a graph and run the query and add them to the new graph
def run_query(file, var):
    g = rdflib.Graph().parse(file)

    # when cannot read the ttl file
    if len(g) == 0:
        return

    q = f"""
        prefix crm: <http://www.cidoc-crm.org/cidoc-crm/> 

        SELECT DISTINCT ?s WHERE{{
            ?s a {var}
        }}
    """

    return len(g.query(q)), len(g)


def count_total(file):
    df = pandas.read_csv(file)
    print(f"Total instance found: {df['instance_count'].sum()} and total graph length: {df['g_stmt_len'].sum()}")


def print_stat(directory: str, entity_type: list[str]):
    stat_table = pandas.DataFrame(columns=["file_name", "instance_count", "g_stmt_len"])

    # TODO handle more than one entity type

    try:
        for subdir, dirs, files in os.walk(directory):
            files = [f for f in files if f.endswith(".ttl")]
            for file in sorted(files, key=lambda s: int(s.split("-")[-1].split(".")[-2])):
                if file is None:
                    continue
                for entity in entity_type:
                    instance_len, g_stmt_len = run_query(directory + "/" + file, entity)
                    temp_df = pandas.DataFrame([[file, instance_len, g_stmt_len]],
                                               columns=["file_name", "instance_count", "g_stmt_len"])
                    stat_table = pandas.concat([stat_table, temp_df], ignore_index=True)

    finally:
        # show dataframe
        print(stat_table.to_string())
        stat_table.to_csv(path_or_buf=os.path.join(directory, "..", "stat", entity_type[0]+".csv"), sep=',')

        count_total(os.path.join(directory, "..", "stat", entity_type[0]+".csv"))


def property_description(directory: str, entity_type: list[str]):
    pass