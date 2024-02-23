## Data Conversion and upload steps
1. [convert_csv2rdf](convert_csv2rdf) script convert csv files into nq files based on the conversion metadata specifciations of the csv files in folder [conversion_metadata](conversion_metadata). 
     - To run this script you need to provide path-to-directory where your csv and metadata is stored.
     - convert_csv_to_rdf() expects your csv and conversion metadata json file is in the same folder.
2.  enrich data with the [enrich_data_bronbeek](enrich_data_bronbeek) script to add provenance activity (i.e., acqusition events, former owner and objects related to person.)
3. compress the .nq files with bash command
   ```bash
   gzip <path-to-folder>/*.nq
   ```
4. [void.ttl](void.ttl) expects triple files are in the same folder as this void.ttl is is.