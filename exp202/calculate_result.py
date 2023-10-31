import pandas


def recall(df, ground_truth):
    true_positive = 0
    for index, row in df.iterrows():
        if row['ConstituentID'] in ground_truth.loc[ground_truth['nmvw_uri'] == row['nmvw_uri']]['ConstituentID'].values:
            true_positive += 1

    r = true_positive/len(ground_truth)

    print(f"Total correspondence: {len(ground_truth)} \nTrue positive count: {true_positive}")
    print(f"Recall: {r}")
    print(f"\n")

    return r, len(ground_truth)


# precision = number of correct correspondence / total retrieved
# precision = true positive / (true positive + false positive)
def precision(df, ground_truth):
    total_retrieved = len(df)
    true_positive = 0

    for index, row in df.iterrows():
        if row['ConstituentID'] in ground_truth.loc[ground_truth['nmvw_uri'] == row['nmvw_uri']]['ConstituentID'].values:
            true_positive += 1

    try:
        p = true_positive / total_retrieved
    except ZeroDivisionError:
        print(f"The total retrieved is: {total_retrieved}!!!!")

    print(f"Total correspondence: {len(df)}\nTotal retrieved: {total_retrieved}\nTrue positive count: {true_positive} ")
    print(f"Precision: {p}")
    print(f"\n")

    return p, true_positive, total_retrieved


def f_measure(recall, precision):
    try:
        f = 2 * (precision * recall)/(precision + recall)
        print(f"F-measure: {f}\n")
        return f
    except ZeroDivisionError:
        print(f"Both precision is {precision} and recall is {recall}!!!")
        return 0


def calculate_result(df, ground_truth):
    # df = pandas.read_pickle(file)
    r, total = recall(df, ground_truth)
    p, correct, retrieved = precision(df, ground_truth)
    f = f_measure(r, p)

    return total, retrieved, correct, r, p, f