from py4j.java_gateway import JavaGateway
import os
import time
from utilities.FileUtilities import FileUtilities


class MyHDT:
    FILE_UTILS = FileUtilities()
    def __init__(self, input_rdf, output_dir):
        try:
            base_uri = "file://" + input_rdf
            file_name = os.path.splitext(os.path.basename(input_rdf))[0]
            output_hdt = os.path.join(output_dir, file_name + ".hdt")

            start_time = time.time()
            notation = rdf_guess_format(input_rdf)
            if notation is None:
                raise ValueError("Could not guess notation for {}. Trying NTriples...".format(input_rdf))
            hdt = HDTDocument(input_rdf, base_uri, notation, '.')

            print("START: Generating HDT dataset...")
            hdt.save_to_hdt(output_hdt, '.')

            print("HDT generated and saved at {}".format(output_hdt))
            print("Time taken: {:.2f} seconds".format(time.time() - start_time))

            start_time = time.time()
            print("START: Generating HDT index...")
            hdt.generate_index()

            print("Index generated and saved at: {}.index".format(output_hdt))
            print("Time taken: {:.2f} seconds".format(time.time() - start_time))

            hdt.close()
        except Exception as e:
            print("Problem generating HDT file")
            print(str(e))

# Example usage:
# my_hdt_instance = MyHDT("path/to/input.rdf", "output_directory")
