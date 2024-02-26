## Data Conversion
[convert_csv2rdf](convert_csv2rdf.py) script convert csv files into nq files based on the conversion metadata specifciations of the csv files in folder [conversion_metadata](conversion_metadata). 
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