Diagram: https://drive.google.com/file/d/16X1PiVgtSVrZNMkEIWW3eY17JztUH5w4/view?usp=sharing 

## Data Conversion


#### Input 
- csv files 
```
		AccessionMethods.csv
		Constituents.csv
		ConXrefDetails.csv
		ConXrefs.csv
		HistEvents.csv
      ObjAccession.csv
      Objects.csv
      ObjectStatuses.csv
      Roles.csv
      RoleTypes.csv
```
- Location path : [local](/Users/sarah_shoilee/Desktop/Sarah.nosync/Bronbeek_Data/) / [cloud](https://vu.data.surfsara.nl/index.php/f/142262424)



#### Create CSV2RDF mapping
   - Write conversion Metadata
     - Generate the conversion blueprint with cow_tool build
   ```
      cow_tool build myfile.csv
   ```
-  update mapping for conversion (follow the steps mentioned [here](https://github.com/Shoilee/dh_entity_linking_v2/blob/serendipity/data_preparation/bronbeekdataConversion/cow_process.md))

#### Conversion to RDF
[convert_csv2rdf](convert_csv2rdf.py) script convert csv files into nq files based on the conversion metadata specifciations of the csv files in folder [conversion_metadata](conversion_metadata). 
     - To run this script you need to provide path-to-directory where your csv and metadata is stored.

`Note: convert_csv2rdf.convert_csv_to_rdf() expects your csv and conversion metadata json file is in the same folder.`

#### Output
RDF Files (format: .nt)


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

TODO: update the data location path