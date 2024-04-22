import os
import re
import glob
import logging
from .LoggingUtilities import LoggingUtilities


class FileUtilities:
    lg = logging.getLogger(None)
    LOG = LoggingUtilities(lg)

    @staticmethod
    def check_if_file_exists(path: str) -> bool:
        if path is not None:
            if not os.path.isdir(path):
                if os.path.exists(path):
                    return True
                else:
                    FileUtilities.LOG.log_error("check_if_file_exists", "File does not exist")
            else:
                FileUtilities.LOG.log_error("check_if_file_exists", "A directory is chosen instead of a file")
        else:
            FileUtilities.LOG.log_error("check_if_file_exists", "No file path is specified")
        return False

    @staticmethod
    def check_if_directory_exists(path: str) -> bool:
        if path is not None:
            if os.path.isdir(path):
                return True
            else:
                FileUtilities.LOG.log_error("check_if_directory_exists", "Specified path is not a directory")
        else:
            FileUtilities.LOG.log_error("check_if_directory_exists", "No directory path is specified")
        return False

    @staticmethod
    def create_directory(path: str, directory_name: str) -> bool:
        try:
            f = os.path.join(path + "/" + directory_name)
            # if directory already exists
            if os.path.exists(f):
                os.rmdir(f) # remove the existing directory
                os.mkdir(f)  # create directory
            else:
                os.mkdir(f)  # create directory
            return True
        except IOError as e:
            FileUtilities.LOG.log_error(
                "create_directory", f"Error creating directory {path}/{directory_name}"
            )
            e.printStackTrace()
            return False

    @staticmethod
    def delete_file(file_path: str) -> bool:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            else:
                return False
        except IOError as e:
            e.printStackTrace()
            return False

    @staticmethod
    def create_file_stream(path: str):
        try:
            # replicating BufferOutputStream in java
            # TODO: check if it is working properly
            file = open(path, "wb")
            out_stream = open(file.fileno(), "wb", buffering=8192)
            FileUtilities.LOG.log_debug("create_file_stream", f"File created successfully at: {path}")
            return out_stream
        except IOError as ex:
            FileUtilities.LOG.log_error("create_file_stream", "Error creating file stream")
            ex.printStackTrace()
            return None
        finally:
            if 'file' in locals():
                file.close()

    @staticmethod
    def write_to_output_stream(out_stream, message: str) -> bool:
        try:
            out_stream.write(bytes(message, 'utf-8'))
            out_stream.write(bytes("\n", 'utf-8'))
            return True
        except IOError as e:
            FileUtilities.LOG.log_error(
                "write_to_output_stream",
                f"Cannot write following message: {message} to stream: {out_stream}",
            )
            e.printStackTrace()
            return False

    @staticmethod
    def count_lines(file_path: str) -> int:
        count_lines = 0
        try:
            # replicating BufferReader from java
            # TODO: check if this is working properly
            with open(file_path, "r", buffering= 1) as reader:
                while reader.readLine() is not None:
                    count_lines += 1
        except IOError as e:
            e.printStackTrace()
        return count_lines

    @staticmethod
    def get_all_valid_links_file(directory: str, output: bool) -> list[str]:
        considered_files = list()
        try:
            result = glob.glob(directory+".csv")
            for file_name in result:
                if FileUtilities.check_if_valid_links_file(file_name):
                    considered_files.add(file_name)
            if not considered_files.isEmpty():
                if output:
                    FileUtilities.LOG.output_console("Computing the transitive closure for the following files:")
                for considered_file in considered_files:
                    if output:
                        FileUtilities.LOG.output_console("\t" + considered_file)
                return considered_files
            else:
                FileUtilities.LOG.log_error(
                    "get_all_valid_links_file",
                    "Missing a CSV file in the specified directory containing the detected links with the following format: "
                    "(within|between)[-_][bmd][-_][bmd]",
                )

        except IOError as e:
            e.printStackTrace()
            FileUtilities.LOG.log_error(
                "get_all_valid_links_file",
                "Missing a CSV file in the specified directory containing the detected links with the following format: "
                "(within|between)[-_][bmd][-_][bmd]",
            )
        return None

    @staticmethod
    def get_file_name(file_path: str) -> str:
        file_name = os.path.basename(file_path)
        # remove file extension
        return ''.join(str(file_name).split(".")[:-1])

    @staticmethod
    def check_if_valid_links_file(file_path: str) -> bool:
        file_name = str(os.path.basename(file_path))
        file_name_lc = file_name.lower()
        p = re.compile("(within|between)[-_][bmd][-_][bmd]")
        m = p.matcher(file_name_lc)
        # TODO: check what is expected to return from this
        return bool(m)

    @staticmethod
    def check_pattern(name: str, regex: str) -> bool:
        file_name = str(os.path.basename(name))
        file_name_lc = file_name.lower()
        p = re.compile(regex)
        m = p.match(file_name_lc)
        # TODO: check what is expected to return from this
        # m.string would return the file name
        return bool(m)

    @staticmethod
    def check_within_b_d(file_path: str) -> bool:
        regex = "(within)[-_](b)[-_](d)"
        return FileUtilities.check_pattern(file_path, regex)
