import pandas


def construct_deezymatch_data(source_file, destination_file):
    df = pandas.read_pickle(source_file)

    df = df.loc[:, ['name_label', 'wiki_label']]

    new_df = pandas.DataFrame(columns=['name_label', 'wiki_label', 'match'])

    for index, row in df.iterrows():
        for wiki_label in row['wiki_label']:
            temp_df = pandas.DataFrame([[row['name_label'], wiki_label, 'YES']], columns=['name_label', 'wiki_label', 'match'])
            new_df = pandas.concat([new_df, temp_df], ignore_index=True)

    new_df.to_pickle(destination_file)
    new_df.to_csv('data/test/dataset-string-matching_finetune.txt', sep=' ', header=False, index=False)


