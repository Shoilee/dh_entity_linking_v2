import pandas


def convert(string):
    list1 = string.strip('[] ').split('),')
    return [item.strip('[] ') + ")" for item in list1]


df = pandas.read_csv("data/test/wikidata_human_name.tsv", sep="\t")

df = df.loc[:, ['name_label', 'wiki_label']]

for index, row in df.iterrows():
    print(convert(row['wiki_label'])[0])
    # print(", ".join(convert(row['wiki_label'])[0:2]).replace('"', ''))
