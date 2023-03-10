import pandas
import rdflib


def f_measure(recall, precision):
    f = 2 * (precision * recall)/(precision + recall)
    print(f"F-measure: {f}\n")

    return f


def recall(df):
    correct_count = 0
    for index, row in df.iterrows():
        if rdflib.term.URIRef(row['wiki_uri']) in row['retrieved_uri']:
            correct_count += 1

    r = correct_count/len(df)

    print(f"Total query: {len(df)} \nCorrect correspondence count: {correct_count}")
    print(f"Recall: {r}")
    print(f"\n")

    return r


# precision = total correct correspondence / total retrieved uri
# precision = true positive / (true positive + false positive)
def precision(df):
    total_retrieved = 0
    correct_count = 0

    for index, row in df.iterrows():
        # if retrieved_uri is empty --> skip count
        if row['retrieved_uri'] == "[]":
            continue
        for target in row['retrieved_uri']:
            total_retrieved += 1
            if rdflib.term.URIRef(row['wiki_uri']) == target:
                correct_count += 1

    p = correct_count / total_retrieved

    print(f"Total query: {len(df)}\nTotal retrieved: {total_retrieved}\nCorrect correspondence count: {correct_count} ")
    print(f"Precision: {p}")
    print(f"\n")

    return p


def result(file):
    df = pandas.read_pickle(file)
    f_measure(recall(df), precision(df))
