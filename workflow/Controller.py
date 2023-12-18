import os
import sys
import time
import logging

from algorithms.match_exact_string import matchExactString as exact
from algorithms.match_with_abbreviation import match_with_abbreviation as initial
from algorithms.match_surname import matchLastName as surname
from algorithms.match_fuzzy_string import match_fuzzy_string as fuzzy

from utilities.LoggingUtilities import LoggingUtilities
from utilities.FileUtilities import FileUtilities


class Controller:
    FUNCTIONS = [
            "showdatasetstats",
            "converttordf",
            "closure",
            "linkconstituents",
        ]

    # list all the supported entity linking algorithms
    ALGORITHMS = ['exact', 'initial', 'surname', 'fuzzy']

    outputFormatCSV = True

    lg = logging.getLogger(__name__)
    LOG = LoggingUtilities(lg)
    FILE_UTILS = FileUtilities()

    def __init__(self, function, inputDataset, outputDirectory, outputFormat="CSV", algorithm="exact"):
        self.function = function
        self.inputDataset = inputDataset
        self.outputDirectory = outputDirectory
        self.outputFormat = outputFormat
        if not outputFormat.__eq__("CSV"):
            Controller.outputFormatCSV = False
        self.algorithm = algorithm

    def run_program(self):
        if self._check_input_function():
            function_name = self.function.lower()
            if function_name == "showdatasetstats":
                if self._check_input_dataset():
                    pass
                    # TODO: implement how to show statistics
                    # self.output_dataset_statistics()
            elif function_name == "converttordf":
                if self._check_input_directory():
                    self.convert_csv_to_rdf(self.inputDataset)
            elif function_name == "linkconstituents":
                if self._check_all_user_inputs():
                    # TODO: convert rdf to dataframe
                    start_time = time.time()
                    # TODO: implement the following functions
                    self.lg.info(f"START: {self.function}")
                    getattr(self, self.algorithm)()
                    Controller.LOG.output_total_runtime(self.algorithm, start_time, True)
            elif function_name == "closure":
                if self._check_input_dataset() and self._check_input_directory_contents():
                    start_time = time.time()
                    self.lg.info("START: Computing the transitive closure")
                    self.compute_closure()
                    Controller.LOG.output_total_runtime(
                        "Computing the transitive closure", start_time, True
                    )
            else:
                Controller.LOG.log_error(
                    "run_program",
                    "User input is correct, but no corresponding function exists (error in code)",
                )

    # ========= input checks =========
    def _check_all_user_inputs(self):
        valid_inputs = True
        valid_inputs &= self._check_input_dataset()
        valid_inputs &= self._check_input_directory()
        self._check_output_format_rdf()
        return valid_inputs

    def _check_input_function(self):
        if self.function is None:
            Controller.LOG.log_error(
                "check_input_function",
                "Missing user input for parameter: --function",
                f"Choose one of the following options: {Controller.FUNCTIONS}",
            )
            return False
        else:
            function_name = self.function.lower()
            print(function_name)
            if function_name in Controller.FUNCTIONS:
                Controller.LOG.log_debug(
                    "check_input_function",
                    f"User has chosen function: {function_name}",
                )
                return True
            Controller.LOG.log_error(
                "check_input_function",
                "Incorrect user input for parameter: --function",
                f"Choose one of the following options: {Controller.FUNCTIONS}",
            )
            return False

    def _check_input_dataset(self, file_url=None):
        if not file_url:
            if "," in self.inputDataset:
                inputs = self.inputDataset.split(",")
                check = self._check_input_dataset(inputs[0])
                check &= self._check_input_dataset(inputs[1])
                self.doubleInputs = True
                return check
            else:
                return self._check_input_dataset(self.inputDataset)
        if Controller.FILE_UTILS.check_if_file_exists(os.path.join("..",file_url)):
            Controller.LOG.log_debug(
                "check_input_file_input",
                f"The following dataset is set as input dataset: {self.inputDataset}",
            )
            return True
        else:
            suggested_fix = (
                "A valid HDT file, or two valid HDT files separated only by a comma "
                "(without a space) are required as input after parameter: --inputData"
            )
            Controller.LOG.log_error(
                "check_input_file_input",
                "Invalid or Missing user input for parameter: --inputData",
                suggested_fix,
            )
            return False

    def _check_input_directory(self):
        if Controller.FILE_UTILS.check_if_directory_exists(self.outputDirectory):
            Controller.LOG.log_debug(
                "check_input_directory_output",
                f"The following directory is set to store results: {self.outputDirectory}",
            )
            return True
        else:
            Controller.LOG.log_error(
                "check_input_directory_output",
                "Invalid or Missing user input for parameter: --outputDir",
                "A valid directory for storing links is required as input after parameter: --outputDir",
            )
            return False

    def _check_input_directory_contents(self):
        if self._check_input_directory():
            if Controller.FILE_UTILS.get_all_valid_links_file(
                self.outputDirectory, False
            ) is not None:
                return True
        return False

    def _check_output_format_rdf(self):
        if self.outputFormatCSV:
            Controller.LOG.log_debug("check_output_format_csv", "Output format is set as CSV")
            Controller.LOG.output_console("converting csv file to rdf")

        else:
            Controller.LOG.log_debug("check_output_format_csv", "Output format is set as RDF")
        return self.outputFormatCSV

    def convert_csv_to_rdf(self, input_file):
        from cow_csvw.csvw_tool import COW
        from rdflib import ConjunctiveGraph

        print(os.getcwd())

        # now URIs are created based on _row_id, it should be based on ConstituentID
        COW(mode='build', files=[input_file], base='http://example.org/'+os.path.basename(self.inputDataset))
        COW(mode='convert', files=[input_file], processes=4, chunksize=100, base='http://example.org/'+os.path.basename(self.inputDataset), gzipped=False)

        # converting nquads to ttl
        g = ConjunctiveGraph()
        g.parse(os.path.join(os.path.dirname(input_file),
                             os.path.basename(input_file)+".nq"), format="nquads")

        g.serialize(destination=os.path.join(os.path.dirname(input_file),
                                             os.path.basename(input_file) + ".ttl"))
