Diagram: https://drive.google.com/file/d/16X1PiVgtSVrZNMkEIWW3eY17JztUH5w4/view?usp=sharing 

## Data Extraction and Conversion

### Wereldmuseum (formerly known as NMVW) data extraction
Using this [script](nmvwdatadump/data_dump.py), Wereldmuseum data was extracted from a remote server.

`run` function retrieves data from an endpoint by making API requests with specified ranges. It saves the response data as files in the `nmvw_data' directory, organized by the specified component. The function loops through the entire data range, making consecutive API calls until it reaches or exceeds the highest value. It handles various exceptions that may occur during the process, such as network errors, empty responses, and conversion errors. It logs encountered errors to separate text files for further analysis.

```
def run(component, highest_value, range, start_limit=1):
    """
    Extract data from an endpoint and store it in files.

    :param component: (str) Specifies which component to access from the endpoint.
    :param highest_value: (int) The possible highest number for the component range.
    :param range: (int) The range of data to request in each API call.
    :param start_limit: (int) Default is 1; indicates the starting range value for the GET request.
    """
```
Example usage:
```run(component='ccrdfconst', highest_value=58000, range=20)```

### Bronbeek Data Conversion
[convert_csv2rdf](bronbeekdataconversion/dataConversion/convert_csv2rdf.py) script convert csv files into nq files based on the conversion metadata specifciations of the csv files in folder [conversion_metadata](conversion_metadata). 
     - To run this script you need to provide path-to-directory where your csv and metadata is stored.


> Note: convert_csv2rdf.convert_csv_to_rdf() expects your csv and conversion metadata json file is in the same folder.



## Upload to cliopatria

1. compress the .nq files with bash command
   ```bash
   gzip <path-to-folder>/*.nq
   ```

2. from cliopatria CLI, type
   ```
   # attach the libraries
   rdf_library:rdf_attach_library(<path-to-folder-of-void.ttl>).
   ```
> Note: [void.ttl](void.ttl) expects triple files are in the same folder as void.ttl.
   ```
   # upload files by library
   rdf_load_library('<library-name>').
   e.g., rdf_library:rdf_load_library('bronbeek').
   ```

## Data Enrichment
Linked data enrichment with the [enrich_data_bronbeek](enrich_data_bronbeek) script to add provenance activity (i.e., acqusition events, former owner and objects related to person.)

```bash
python enrich_data_bronbeek.py <folder-path-of-all-nq-files>
```
> [enrich_data_bronbeek.py](enrich_data_bronbeek.py) expects .nq files.


## Data 
1. [Bronbeek]() (format: csv)
2. [NMVW](https://surfdrive.surf.nl/files/index.php/apps/files/?dir=/Shared/Work%20Package%201B/data/linkedart_nmvw_data/ccrdfconst&fileid=12458101919) (format: rdf/ttl)