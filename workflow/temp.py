# ========= utilities =========
def convert_to_hdt(self, s):
    if "," in self.inputDataset:
        print(f"Input Dataset: {self.inputDataset}")
        inputs = self.inputDataset.split(",")
        if (
                self._check_input_dataset(inputs[0])
                and self._check_input_dataset(inputs[1])
        ):
            MyHDT(inputs[0], inputs[1], self.outputDirectory)
    else:
        if self._check_input_dataset():
            MyHDT(self.inputDataset, self.outputDirectory)


# ========= functions =========
def output_dataset_statistics(self):
    formatter = "{:,}"
    if self.doubleInputs:
        inputs = self.inputDataset.split(",")
        my_hdt = MyHDT(inputs[0], inputs[1], self.doubleInputs)
    else:
        my_hdt = MyHDT(self.inputDataset)
    number_of_birth_events = my_hdt.get_number_of_subjects(TYPE_BIRTH_EVENT)
    self.LOG.output_console(
        f"--- 	# Birth Events: {formatter.format(number_of_birth_events)} ---"
    )
    number_of_marriage_events = my_hdt.get_number_of_subjects(TYPE_MARRIAGE_EVENT)
    self.LOG.output_console(
        f"--- 	# Marriage Events: {formatter.format(number_of_marriage_events)} ---"
    )
    number_of_death_events = my_hdt.get_number_of_subjects(TYPE_DEATH_EVENT)
    self.LOG.output_console(
        f"--- 	# Death Events: {formatter.format(number_of_death_events)} ---"
    )
    number_of_individuals = my_hdt.get_number_of_subjects(TYPE_PERSON)
    self.LOG.output_console(
        f"--- 	# Individuals: {formatter.format(number_of_individuals)} ---"
    )
    my_hdt.close_dataset()


def within_b_d(self):
    options = self.LOG.get_user_options(
        self.maxLev, self.fixedLev, self.singleInd, self.ignoreDate, self.ignoreBlock
    )
    dir_name = f"{self.function}{options}"
    process_dir_created = self.FILE_UTILS.create_directory(
        self.outputDirectory, dir_name
    )
    if process_dir_created:
        main_directory = os.path.join(self.outputDirectory, dir_name)
        dictionary_dir_created = self.FILE_UTILS.create_directory(
            main_directory, DIRECTORY_NAME_DICTIONARY
        )
        database_dir_created = self.FILE_UTILS.create_directory(
            main_directory, DIRECTORY_NAME_DATABASE
        )
        results_dir_created = self.FILE_UTILS.create_directory(
            main_directory, DIRECTORY_NAME_RESULTS
        )
        if (
                dictionary_dir_created
                and database_dir_created
                and results_dir_created
        ):
            my_hdt = MyHDT(self.inputDataset)
            Within_B_D(
                my_hdt,
                main_directory,
                self.maxLev,
                self.fixedLev,
                self.ignoreDate,
                self.ignoreBlock,
                self.singleInd,
                self.outputFormatCSV,
            )
            my_hdt.close_dataset()
        else:
            self.LOG.log_error(
                "within_b_d",
                "Error in creating the three sub output directories",
            )
    else:
        self.LOG.log_error(
            "within_b_d", "Error in creating the main output directory"
        )


def compute_closure(self):
    dir_name = self.function
    process_dir_created = self.FILE_UTILS.create_directory(
        self.outputDirectory, dir_name
    )
    if process_dir_created:
        main_directory = os.path.join(self.outputDirectory, dir_name)
        database_dir_created = self.FILE_UTILS.create_directory(
            main_directory, DIRECTORY_NAME_DATABASE
        )
        results_dir_created = self.FILE_UTILS.create_directory(
            main_directory, DIRECTORY_NAME_RESULTS
        )
        if database_dir_created and results_dir_created:
            my_hdt = MyHDT(self.inputDataset)
            Closure(
                my_hdt,
                self.outputDirectory,
                self.outputFormatCSV,
            )
            my_hdt.close_dataset()
        else:
            self.LOG.log_error(
                "Closure", "Error in creating the main output directory"
            )
