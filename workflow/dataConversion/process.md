1. Locate the csv file
2. run cow_tool build --> <filename>-metadata.json file is created
   ```
   cow_tool build myfile.csv
   ```
3. Curate the json based on schema of the linked data
   1. change base uri
   2. add desired prefixes, if not present. e.g., 
        "la": "https://linked.art/ns/terms/" ,
   3. I am not manupulating the data types too much
   4. ?s ?p ?o
      1. [Subject](https://github.com/CLARIAH/COW/wiki/1.-Adapting-the-Metadata#subject-abouturl) (aboutURL)
         - Change "aboutUrl" to manupulate subject URIs
             e.g. "aboutUrl": "{ConstituentID}"; where "ConstituentID" is the primary key of the given table
      2. [Predicate](https://github.com/CLARIAH/COW/wiki/1.-Adapting-the-Metadata#predicate-propertyurl) (propertyURL)
         - You can specify predicate by "propertyURL" and specify the value using "valueURL"
         - e.g., 
            ```
            {
                "name": "properties_name_in_uri",
                "datatype": "string",
                "dc:description": "Name of neighbourhood as described in the dataset",
                "titles": ["Property name of neighbourhood in the URI"],
                "propertyUrl": "rdf:type",
                "valueUrl": "sdmx-dimension:refArea",
                "@id": "https://iisg.amsterdam/buurt.csv/column/properties_name_in_uri"
            },
            ```
      3. [Object](https://github.com/CLARIAH/COW/wiki/1.-Adapting-the-Metadata#object-valueurl--csvwvalue) (valueURL / CSVW:value)
         - altering "CSVW:value" or "valueUrl" we can specify the object value in a desired format
         - e.g., 
          ```
         "name": "Dienstboden",
            ...,
            "propertyUrl": "vocab/averageNrMaids",
            "CSVW:value": "{{Dienstboden|replace(',', '.')}}",
            "@id": "https://iisg.amsterdam/buurt.csv/column/Dienstboden"
         ```
4. run cow_tool convert --> <filename>.nq file is created
   ```
   cow_tool convert myfile.csv
   ```
5. sort <filename>csv.nq > <filename>_sorted.csv.nq
