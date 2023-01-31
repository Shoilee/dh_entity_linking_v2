import pandas

# TODO json would be much more suitable for caching
# TODO calculate the correct correspondence
# TODO two variable count and correct



# TODO add F1 measure
def F1_measure(df):
    pass


def accuracy(df):
    pass


def recall(df):
    correct_count = 0
    for index, row in df.iterrows():
        if row['wiki_uri'] in row['retrieved_uri']:
            correct_count += 1

    print(f"Total query: {len(df)} \nretrieved {correct_count}")
    print(f"Recall: {correct_count/len(df)}")
    print(f"\n")


# TODO change the word 'found' with 'retrieved'
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
            if row['wiki_uri'] == target:
                correct_count += 1

    print(f"Total query: {len(df)}\nTotal retrieved: {total_retrieved}\nCorrect correspondence count: {correct_count} ")
    print(f"Precision: {correct_count / total_retrieved}")
    print(f"\n")


def result(file):
    df = pandas.read_pickle(file)

    # accuracy(df)
    recall(df)
    precision(df)
