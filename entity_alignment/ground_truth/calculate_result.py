import pandas


def recall(df):
    correct_count = 0
    for index, row in df.iterrows():
        if len(set(row['retrieved_names']).intersection(set([str(item) for item in row['wiki_label']]))) > 0:
            correct_count += 1

    r = correct_count/len(df)

    print(f"Total query: {len(df)} \nCorrect correspondence count: {correct_count}")
    print(f"Recall: {r}")
    print(f"\n")

    return r, len(df)


# p = total correct correspondence / total retrieved uri
# p = true positive / (true positive + false positive)
def precision(df):
    total_retrieved = 0
    correct_count = 0
    false_count = 0

    import numpy as np

    for index, row in df.iterrows():
        if len(set(row['retrieved_names']).intersection(set([str(item) for item in row['wiki_label']]))) > 0:
            correct_count += 1
        for name in row['retrieved_names']:
            if name not in row['wiki_label']:
                false_count += 1
        total_retrieved = correct_count + false_count

    """
    for index, row in df.iterrows():
        # if retrieved_names is empty --> skip count
        if row['retrieved_names'] == "[]":
            continue
        for target in row['retrieved_names']:
            total_retrieved += 1
            if target in [str(item) for item in row['wiki_label']]:
                correct_count += 1
    """

    try:
        p = correct_count / total_retrieved
    except ZeroDivisionError:
        print(f"The total retrieved is: {total_retrieved}!!!!")

    print(f"Total query: {len(df)}\nTotal retrieved: {total_retrieved}\nCorrect correspondence count: {correct_count} ")
    print(f"Precision: {p}")
    print(f"\n")

    return p, correct_count, total_retrieved


def f_measure(recall, precision):
    try:
        f = 2 * (precision * recall)/(precision + recall)
        print(f"F-measure: {f}\n")
        return f
    except ZeroDivisionError:
        print(f"Both precision is {precision} and recall is {recall}!!!")
        return 0


def calculate_result(file):
    df = pandas.read_pickle(file)
    r, total = recall(df)
    p, correct, retrieved = precision(df)
    f = f_measure(r, p)

    return total, retrieved, correct, r, p, f