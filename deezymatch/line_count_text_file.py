def text_file_count(file="data/deezymatch/dataset-candidates.txt"):
    with open(file, 'r') as fp:
        for count, line in enumerate(fp):
            pass
    print('Total Lines', count + 1)