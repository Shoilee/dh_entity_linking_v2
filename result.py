import pandas

# TODO json would be much more suitabable for caching

# TODO calculate the correct correspondence
# TODO two variable count and correct
# precision is found / count
# TODO add F1 measure


def accuracy(df):
    pass


def recall(df):
    count = 0
    for index, row in df.iterrows():
        if row['wiki_uri'] in row['found_uri']:
            count += 1

    print(f"Total query: {len(df)} and retrieved {count}")
    print(f"Recall: {count/len(df)}")
    print(f"\n")


def precision(df):
    found = 0
    count = 0

    # TODO number of correct

    for index, row in df.iterrows():
        for target in row['found_uri'].split(','):
            print(target)
    """
            if row['wiki_uri'] == target:
                found += 1
        if  len(row['found_uri'].split(",")) ==1 :
            pass

    print(f"Total query: {len(df)} and found {count}")
    print(f"Precision: {count / len(df)}")
    print(f"\n")
    """




def result(file):
    df = pandas.read_csv(file, sep="\t")
    print(type(df['found_uri'][0].split(',')))

    # accuracy(df)
    # recall(df)
    precision(df)
