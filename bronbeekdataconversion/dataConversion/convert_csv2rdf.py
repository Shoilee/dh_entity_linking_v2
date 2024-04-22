import os
from cow_csvw.csvw_tool import COW


def convert_csv_to_rdf(directory):
    for root, _, f in os.walk(directory):
        f = [file for file in f if file.endswith(('.csv'))]
        print(f)
        for file in f:
            COW(mode='convert', files=[os.path.join(root, file)], processes=4, chunksize=100, base='http://pressingmatter.nl/Bronbeek/'+os.path.basename(file), gzipped=False)


# TODO: place the sample csv in `data` directory
if __name__=="__main__":
    convert_csv_to_rdf("data/")