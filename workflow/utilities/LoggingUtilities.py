import logging, time
# TODO: if this code throws error or unexpected output deal with this;
#  as it has been converted from java code to python using ChatGPT


class LoggingUtilities:
    def __init__(self, log=None):
        self.LOG = log

    def output_console(self, message):
        print(message)

    def log_debug(self, function, message):
        self.LOG.debug(
            f"\n\tFUNCTION -> {function}"
            f"\n\tDEBUG -> {message}"
            f"\n -----"
        )

    def log_warn(self, function, message, suggestion=None):
        if suggestion is not None:
            self.LOG.warn(
                f"\n\tFUNCTION -> {function}"
                f"\n\tWARNING -> {message}"
                f"\n\tFIX --> {suggestion}"
                f"\n -----"
            )
        else:
            self.LOG.warn(
                f"\n\tFUNCTION -> {function}"
                f"\n\tWARNING -> {message}"
                f"\n -----"
            )

    def log_error(self, function, message, suggestion=None):
        if suggestion is not None:
            self.LOG.error(
                f"\n\tFUNCTION -> {function}"
                f"\n\tERROR -> {message}"
                f"\n\tFIX -> {suggestion}"
                f"\n -----"
            )
        else:
            self.LOG.error(
                f"\n\tFUNCTION -> {function}"
                f"\n\tERROR -> {message}"
                f"\n -----"
            )

    def output_total_runtime(self, process_name: str, start_time, output: bool):
        end_time = time.time()
        total_time = round((end_time - start_time), 2)
        total_time_minutes = round(total_time / 60, 2)

        message = f"*DONE: {process_name}"

        if total_time > 1:
            if total_time_minutes > 1:
                message += f" [runtime: {total_time} s / {total_time_minutes} m]"
            else:
                message += f" [runtime: {total_time} s]"

        if output:
            self.output_console(message)

        return message

    def get_user_options(self, max_lev, fixed_lev, single_ind, ignore_date, ignore_block):
        options = f"-maxLev-{max_lev}"

        if fixed_lev:
            options += "-fixed"
        if single_ind:
            options += "-singleInd"
        if ignore_date:
            options += "-ignoreDate"
        if ignore_block:
            options += "-ignoreBlock"

        return options

