import rdflib
import os
from tqdm import tqdm


def merge_graph(directory, outputDir):
    """
    Given a directory, it walk over all the file with '.ttl' extension and merges them in a single file
    @param directory: the path to folder contains the .ttl file
    @param outputDir: path location for storing the complied Graph file
    @return: NULL; just store the complied graph file in the output directory
    """
    new_graph = rdflib.Graph()

    try:
        for subdir, dirs, files in os.walk(directory):
            files = [f for f in files if f.endswith(".ttl")]
            for file in tqdm(sorted(files, key=lambda s: int(s.split("-")[-1].split(".")[-2]))):
                current_graph = rdflib.Graph().parse(os.path.join(directory, file))
                new_graph = new_graph + current_graph
    finally:
        new_graph.serialize(destination=os.path.join(outputDir, 'all_constituents.ttl'), format='ttl')


if __name__ == "__main__":
    merge_graph('/Users/sarah_shoilee/PycharmProjects/entity_linking/nmvw_data/ccrdfconst',
                '/Users/sarah_shoilee/PycharmProjects/entity_linking/nmvw_data')