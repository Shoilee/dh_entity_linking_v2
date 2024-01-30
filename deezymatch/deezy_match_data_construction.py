import pandas
import string
import random
import os
import pickle
import random
from thefuzz import fuzz


def construct_deezymatch_data(source_file, directory="deezymatch/data/"):
    df = pandas.read_pickle(source_file)

    # DICTIONARY MAPS ID TO ALL DIFFERENT NAME VARIANTS
    id_to_names = dict()
    for i, row in df.iterrows():
        id = row['wiki_uri'].toPython()
        altnames = list(set([row['name_label'].value] + [label.value for label in row["wiki_label"]]))
        id_to_names[id] = altnames

    with open(directory+'id_to_names.pickle', 'wb') as file:
        pickle.dump(id_to_names, file, protocol=pickle.HIGHEST_PROTOCOL)

    # DICTIONARY MAPS NAME VARIATION TO ITS ID
    name_to_id = dict()
    for id in id_to_names:
        for name in id_to_names[id]:
            if name in name_to_id:
                name_to_id[name].append(id)
            else:
                name_to_id[name] = [id]

    with open(directory+'name_to_id.pickle', 'wb') as file:
        pickle.dump(name_to_id, file, protocol=pickle.HIGHEST_PROTOCOL)

    # GET ALL DIFFERENT NAMES
    all_names = []
    for k in id_to_names:
        if type(id_to_names[k]) == list:
            all_names += id_to_names[k]

    all_names = list(set(all_names))

    # Utils: map punctuation to white spaces, for token-based Jaccard similarity needed below:
    punctuation = string.punctuation + "’"
    translator = str.maketrans(string.punctuation, ' ' * len(string.punctuation))

    # Get positive matches from Geonames pairs of names, if
    # their similarity is > 0.60 or if Jaccard similarity of its
    # tokens is larger than 0.5:
    positive_matches = []
    for k in id_to_names:
        if type(id_to_names[k]) == list:
            for name1 in id_to_names[k]:
                for name2 in id_to_names[k]:
                    # Character-based string similarity:
                    if fuzz.ratio(name1, name2) > 60:
                        positive_matches.append(name1 + "\t" + name2 + "\t" + "TRUE")
                    # Token-based string similarity:
                    else:
                        s1 = set(name1.translate(translator).split(" "))
                        s2 = set(name2.translate(translator).split(" "))
                        if float(len(s1.intersection(s2)) / len(s1.union(s2))) >= 0.5:
                            positive_matches.append(name1 + "\t" + name2 + "\t" + "TRUE")

    # Get negative matches (the same number as positive matches)
    # from Geonames pairs of names, if their string similarity
    # is < 0.40 or if Jaccard similarity of its tokens is less than 0.2:
    negative_matches = []
    while len(negative_matches) < len(positive_matches):
        random_pair = random.choices(all_names, k=2)
        name1 = random_pair[0]
        name2 = random_pair[1]
        # Character-based string similarity:
        if fuzz.ratio(name1, name2) < 40:
            negative_matches.append(name1 + "\t" + name2 + "\t" + "FALSE")
        # Token-based string similarity:
        else:
            s1 = set(name1.translate(translator).split(" "))
            s2 = set(name2.translate(translator).split(" "))
            if float(len(s1.intersection(s2)) / len(s1.union(s2))) < 0.2:
                negative_matches.append(name1 + "\t" + name2 + "\t" + "FALSE")

    # Write string pairs into a file (this is the string matching dataset):
    with open(directory+"name_pairs.txt", "w") as fw:
        for nm in negative_matches:
            fw.write(nm + "\n")
        for pm in positive_matches:
            fw.write(pm + "\n")

    # Shuffle the negative and positive examples
    lines = open(directory+"name_pairs.txt").readlines()
    random.shuffle(lines)
    open(directory+"name_pairs.txt", 'w').writelines(lines)
    open(directory+"dataset-string-matching_train.txt", 'w').writelines(lines)

    # PREPARE THE CANDIDATES DATASET
    # The candidates dataset is created from all toponyms and variations from
    # the country of interest:
    candidates = list(name_to_id.keys())

    # Store the candidates dataset, with one toponym per line
    with open(directory+"candidates.txt", "w") as fw:
        for c in set(candidates):
            fw.write(c + "\n")

    # PREPARE THE QUERIES DATASET
    # all we need is query.txt file where each query text is stored in individual line.

    # Store the queries dataset, with one name per line
    with open(directory+"queries.txt", "w") as fw:
        # chose any random names for query
        # for query in random.choices(df['name_label'], k=100):
        for query in df['name_label']:
            fw.write(query + "\n")


def generate_test_data(source_file, directory):
    df = pandas.read_pickle(source_file)

    # DICTIONARY MAPS ID TO ALL DIFFERENT NAME VARIANTS
    id_to_names = dict()
    for i, row in df.iterrows():
        id = row['wiki_uri'].toPython()
        altnames = list(set([row['name_label']] + [label for label in row["wiki_label"]]))
        id_to_names[id] = altnames

    with open(directory+'id_to_names.pickle', 'wb') as file:
        pickle.dump(id_to_names, file, protocol=pickle.HIGHEST_PROTOCOL)

    # DICTIONARY MAPS NAME VARIATION TO ITS ID
    name_to_id = dict()
    for id in id_to_names:
        for name in id_to_names[id]:
            if name in name_to_id:
                name_to_id[name].append(id)
            else:
                name_to_id[name] = [id]

    with open(directory+'name_to_id.pickle', 'wb') as file:
        pickle.dump(name_to_id, file, protocol=pickle.HIGHEST_PROTOCOL)

    # PREPARE THE CANDIDATES DATASET
    # The candidates dataset is created from all toponyms and variations from
    # the country of interest:
    candidates = list(name_to_id.keys())

    # Store the candidates dataset, with one toponym per line
    with open(directory+"candidates.txt", "w") as fw:
        for c in set(candidates):
            fw.write(c + "\n")

    # PREPARE THE QUERIES DATASET
    # all we need is query.txt file where each query text is stored in individual line.

    # Store the queries dataset, with one name per line
    with open(directory+"queries.txt", "w") as fw:
        # chose any random names for query
        # for query in random.choices(df['name_label'], k=100):
        for query in df['name_label']:
            fw.write(query + "\n")


