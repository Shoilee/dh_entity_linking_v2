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
    correspondence_count = 0
    for index, row in df.iterrows():
        if row['wiki_uri'] in row['found_uri']:
            correspondence_count += 1

    print(f"Total query: {len(df)} \nretrieved {correspondence_count}")
    print(f"Recall: {correspondence_count/len(df)}")
    print(f"\n")


# TODO change the word 'found' with 'retrieved'
# precision = total correct correspondence / total retrieved uri
# precision = true positive / (true positive + false positive)
def precision(df):
    total_retrieved = 0
    correspondence_count = 0

    for index, row in df.iterrows():
        # if found_uri is empty --> skip count
        if row['found_uri'] == "[]":
            continue
        for target in row['found_uri'].split(','):
            total_retrieved += 1
            if row['wiki_uri'] in target:
                correspondence_count += 1

    print(f"Total query: {len(df)}\nTotal retrieved: {total_retrieved}\nCorrect correspondence count: {correspondence_count} ")
    print(f"Precision: {correspondence_count / total_retrieved}")
    print(f"\n")


def result(file):
    df = pandas.read_csv(file, sep="\t")

    # accuracy(df)
    recall(df)
    precision(df)
