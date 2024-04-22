import logging
import sys
import time
from argparse import ArgumentParser

from utilities.LoggingUtilities import LoggingUtilities
from utilities.FileUtilities import FileUtilities
from Controller import Controller


class App:
    def __init__(self):
        self.function = None
        self.input_data = None
        self.output_dir = None
        self.format = "CSV"
        self.help = False
        self.debug = "error"

        self.lg = logging.getLogger(None)
        self.LOG = LoggingUtilities(self.lg)

    def parse_arguments(self, argv):
        parser = ArgumentParser(add_help=False)
        parser.add_argument("--function", dest="function")
        parser.add_argument("--inputData", dest="input_data")
        parser.add_argument("--outputDir", dest="output_dir")
        parser.add_argument("--format", dest="format", default="CSV")
        parser.add_argument("--help", dest="help", action="store_true")
        parser.add_argument("--debug", dest="debug", default="error")

        args = parser.parse_args(argv)

        self.function = args.function
        self.input_data = args.input_data
        self.output_dir = args.output_dir
        self.format = args.format
        self.help = args.help
        self.debug = args.debug

    def run(self):
        self.LOG.output_console("")
        self.LOG.output_console("=======================")
        self.LOG.output_console("Welcome to Entity Linking")
        self.LOG.output_console("=======================")
        self.LOG.output_console("")
        start_time = time.time()

        # Set logging level
        logging.basicConfig(level=logging.ERROR)

        if not self.help:
            if self.debug == "warn":
                logging.basicConfig(level=logging.ERROR)
            elif self.debug == "all":
                logging.basicConfig(level=logging.DEBUG)

            # TODO: fix the controller file
            cntrl = Controller(self.function, self.input_data, self.output_dir, self.format)
            cntrl.run_program()
        else:
            # Display help message
            formatting = "\t"
            #formatting = "%-18s %15s %n"
            print("Parameters that can be provided as input to the linking tool:")
            print(f"{formatting}--function:, (required) One of the functionalities listed below")
            print(f"{formatting}--inputData:, (required) Path of the HDT dataset")
            print(f"{formatting}--outputDir:, (required) Path of the directory for saving the indices and the detected links")
            print(f"{formatting}--maxLev:,"
                  f"(optional, default = 4) Integer between 0 and 4, indicating the maximum Levenshtein distance per first or last name allowed for accepting a link")
            print(f"{formatting}--fixedLev:, "
                  f"(optional, default = False) Add this flag without a value (i.e. True) for applying the same maximum Levenshtein distance independently from the string lengths")
            print(f"{formatting}--format:",
                  f"(optional, default = CSV) One of the two Strings: 'RDF' or 'CSV', indicating the desired format for saving the detected links between certificates")
            print(f"{formatting}--debug:",
                  f"(optional, default = error) One of the two Strings: 'error' (only display error messages in console) or 'all' (show all warning in console)")
            print("\n")

            print("Functionalities that are supported in the current version: (case insensitive)")
            # Add other functionalities similarly

        # TODO: check if LOG class is operating correctly
        self.LOG.output_console("")
        self.LOG.output_console("=====================")
        self.LOG.output_total_runtime("Entity Linking", start_time, True)
        self.LOG.output_console("=====================")
        self.LOG.output_console("")


if __name__ == "__main__":
    app = App()
    print(sys.argv[1:])
    app.parse_arguments(sys.argv[1:])
    app.run()

