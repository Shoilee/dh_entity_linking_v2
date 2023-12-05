import os
import sys
import time
import logging
from processes import Closure
from utilities.LoggingUtilities import LoggingUtilities
from utilities.FileUtilities import FileUtilities
    #MyHDT


#from iisg.amsterdam.burgerlinker.Properties import (
#    TYPE_BIRTH_EVENT,
#    TYPE_MARRIAGE_EVENT,
#    TYPE_DEATH_EVENT,
#    TYPE_PERSON,
#    DIRECTORY_NAME_DICTIONARY,
#    DIRECTORY_NAME_DATABASE,
#    DIRECTORY_NAME_RESULTS,
#)


class Controller:
    FUNCTIONS_not_implemented = [
            "within_m_d",
            "within_b_b",
            "within_m_m",
            "within_d_d",
            "within_b_m",
            "between_b_m",
            "between_m_m",
            "between_d_m",
            "between_b_d"
        ]
    FUNCTIONS = [
            "showdatasetstats",
            "converttohdt",
            "closure",
            "within_b_d",
        ]

    outputFormatCSV = True

    lg = logging.getLogger(__name__)
    LOG = LoggingUtilities(lg)
    FILE_UTILS = FileUtilities()

    # TODO: introduce the log operation as in the line 25-27 on the original java file
    def __init__(self, function, inputDataset, outputDirectory, outputFormat="CSV",
                 maxLev=0, fixedLev=False, ignoreDate=False, ignoreBlock=False, singleInd=False):
        self.function = function
        self.maxLev = maxLev
        self.fixedLev = fixedLev
        self.ignoreDate = ignoreDate
        self.ignoreBlock = ignoreBlock
        self.singleInd = singleInd
        self.inputDataset = inputDataset
        self.outputDirectory = outputDirectory
        self.outputFormat = outputFormat
        if not outputFormat.__eq__("CSV"):
            Controller.outputFormatCSV = False

    def run_program(self):
        if self._check_input_function():
            function_name = self.function.lower()
            if function_name == "showdatasetstats":
                if self._check_input_dataset():
                    # TODO: we are here
                    self.output_dataset_statistics()
            elif function_name == "converttohdt":
                if self._check_input_directory():
                    # TODO: maybe do convert_to_hdt first
                    self.convert_to_hdt(self.inputDataset)
            elif function_name == "within_b_d":
                if self._check_all_user_inputs():
                    start_time = time.time()
                    self.lg.info(f"START: {self.function}")
                    getattr(self, function_name)()
                    Controller.LOG.output_total_runtime(self.function, start_time, True)
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
        valid_inputs &= self._check_input_max_levenshtein()
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

    def _check_input_max_levenshtein(self):
        if 0 <= self.maxLev <= 4:
            Controller.LOG.log_debug(
                "check_input_max_levenshtein",
                f"User has chosen max Levenshtein distance: {self.maxLev}",
            )
            return True
        else:
            Controller.LOG.log_error(
                "check_input_max_levenshtein",
                "Invalid user input for parameter: --maxlev",
                "Specify a 'maximum Levenshtein distance' between 0 and 4",
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
        else:
            Controller.LOG.log_debug("check_output_format_csv", "Output format is set as RDF")
        return self.outputFormatCSV
