class Person:
    # TODO: check whether the conversion is correct
    names_separator = " "
    compound_name_separator = "_"

    def __init__(self, URI=None, role=None):
        self.URI = URI
        self.role = role
        self.first_name = None
        self.last_name = None
        self.gender = None
        self.valid = False

    def set_first_name(self, first_name):
        self.first_name = first_name

    def set_last_name(self, last_name):
        self.last_name = last_name

    def set_gender(self, gender):
        self.gender = gender

    def get_URI(self):
        return self.URI

    def get_role(self):
        return self.role

    def get_first_name(self):
        if self.first_name is not None:
            modified_first_name = self.first_name.replace(" ", self.compound_name_separator)
            modified_first_name = modified_first_name.replace("-", self.compound_name_separator)
            return modified_first_name
        else:
            return None

    def get_last_name(self):
        if self.last_name is not None:
            modified_last_name = self.last_name.replace(" ", self.compound_name_separator)
            modified_last_name = modified_last_name.replace("-", self.compound_name_separator)
            return modified_last_name
        else:
            return None

    def get_full_name(self):
        full_name = f"{self.get_first_name()}{self.names_separator}{self.get_last_name()}"
        return full_name

    def get_possible_full_name_combinations(self):
        full_names = {}
        first_name = self.get_first_name()
        if self.compound_name_separator in first_name:
            first_names = first_name.split(self.compound_name_separator)
            full_names = self.ordered_combination(first_names, self.get_last_name())
        else:
            full_names[self.get_full_name()] = "1/1"
        return full_names

    def ordered_combination(self, first_names, last_name):
        result = {}
        length = len(first_names)
        copied_first_names = first_names.copy()
        for i in range(length):
            fixed = first_names[i]
            count = 1
            result[f"{fixed}{self.names_separator}{last_name}"] = f"{count}/{length}"
            copied_first_names.remove(fixed)
            for fn in copied_first_names:
                count += 1
                fixed = f"{fixed}{self.compound_name_separator}{fn}"
                result[f"{fixed}{self.names_separator}{last_name}"] = f"{count}/{length}"
        return result

    def get_gender(self):
        return self.gender

    def print_identity(self):
        print("+-------------------------------------------------------------------------------")
        print(f"* Person: {self.URI}")
        print(f" ---> First Name: {self.first_name}")
        print(f" ---> Last Name: {self.last_name}")
        print(f" ---> Role: {self.role}")
        print(f" ---> Gender: {self.gender}")
        print("+-------------------------------------------------------------------------------")

    def has_first_name(self):
        return self.first_name is not None

    def has_last_name(self):
        return self.last_name is not None

    def has_full_name(self):
        if self.first_name is not None and self.first_name != "n":
            if self.last_name is not None:
                return True
        return False

    def is_female(self):
        return self.gender == "f"

    def is_male(self):
        return self.gender == "m"

    def has_gender(self, gender):
        return self.gender == gender or self.gender == "u"

    def has_double_barreled_first_name(self):
        return self.get_first_name() is not None and self.compound_name_separator in self.get_first_name()

    def has_double_barreled_last_name(self):
        return self.get_last_name() is not None and self.compound_name_separator in self.get_last_name()

    def decompose_first_name(self):
        return self.get_first_name().split(self.compound_name_separator) if self.has_double_barreled_first_name() else [self.get_first_name()]

    def decompose_first_name_add_last_name(self):
        result = set()
        if self.has_double_barreled_first_name():
            first_names = self.get_first_name().split(self.compound_name_separator)
            last_name = self.get_last_name()
            result.update(f"{first_name}{self.names_separator}{last_name}" for first_name in first_names)
        else:
            result.add(self.get_full_name())
        return result

    def decompose_last_name(self):
        return self.get_last_name().split(self.compound_name_separator) if self.get_last_name() is not None else []

    def is_valid(self):
        return self.valid

    def is_valid_with_full_name(self):
        return self.is_valid() and self.has_full_name()

    def set_valid(self, valid):
        self.valid = valid

    def get_number_of_first_names(self):
        if self.has_first_name():
            return self.get_first_name().count(self.names_separator) + 1
        return -1
