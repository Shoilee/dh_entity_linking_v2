import pandas


def recall(df, ground_truth):
    all_positive = len(ground_truth)
    true_positive = 0
    for index, row in df.iterrows():
        if row['ConstituentID'] in ground_truth.loc[ground_truth['nmvw_uri'] == str(row['nmvw_uri'])]['ConstituentID'].values:
            # for https://hdl.handle.net/20.500.11840/pi64129 in
            true_positive += 1

    r = true_positive/all_positive

    print(f"All positive count: {all_positive} \nTrue positive count: {true_positive}")
    print(f"Recall: {r}")
    print(f"\n")

    return r, len(ground_truth)


# p = number of correct correspondence / total retrieved
# p = true positive / (true positive + false positive)
def precision(df, ground_truth):
    # total_retrieved = len(df)
    false_positive = 0
    true_positive = 0

    for index, row in df.iterrows():
        if ground_truth[ground_truth['nmvw_uri'] == str(row['nmvw_uri'])].empty:
            continue # if the row['nmvw_uri'] do not match with any ground_truth['nmvw_uri'], DO NOTHING!
        if row['ConstituentID'] in ground_truth.loc[ground_truth['nmvw_uri'] == str(row['nmvw_uri'])]['ConstituentID'].values:
            true_positive += 1
        else:
            print(row)
            print("\n")
            false_positive += 1

        '''
        for _, matched_row in ground_truth[ground_truth['nmvw_uri'] == str(row['nmvw_uri'])].iterrows():
            if matched_row['ConstituentID'] == row['ConstituentID']:
                true_positive += 1
            else:
                print(row)
                false_positive += 1
        '''

    found_positive = true_positive + false_positive
    try:
        p = true_positive / found_positive
    except ZeroDivisionError:
        print(f"Found positive count: {found_positive}!!!!")

    print(f"Total true correspondence: {len(ground_truth)}\n"
          f"Found positive count: {found_positive}\n"
          f"True positive count: {true_positive} ")
    print(f"Precision: {p}")
    print(f"\n")

    return p, true_positive, found_positive


def f_measure(r, p):
    try:
        f = 2 * (p * r) / (p + r)
        print(f"F-measure: {f}\n")
        return f
    except ZeroDivisionError:
        print(f"Both precision is {p} and recall is {r}!!!")
        return 0


def calculate_result(df, ground_truth):
    # df = pandas.read_pickle(file)
    r, total = recall(df, ground_truth)
    p, correct, retrieved = precision(df, ground_truth)
    f = f_measure(r, p)

    return total, retrieved, correct, r, p, f
