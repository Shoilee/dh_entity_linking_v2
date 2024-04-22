# Steps: 
1. Run cow build on the file and generate metadata.json file for conversion
    ```
    cow_tool build <file-path-csv>
    ```
2. modify the metadata.json file with your specification. For more details visit [page](cow_process.md).  
   -  cow-csvw basic propeties:

    ```
    "virtual": true,
    "name": "ObjectName",
    "dc:description": ["captures the class of the object"],
    "datatype": "string",
    "null": ["NULL"],
    "aboutUrl" : "https://example.com/Bronbeek/{ObjectID}/",
    "propertyUrl": "rdf:type",
    "valueUrl": "cidoc:E22_Human-Made_Object",
    "@id": "http://www.cidoc-crm.org/cidoc-crm/E22_Human-Made_Object"
    ```

3. Look into the linkedart specification and modify "objects" and "constituent" metadata
   all the metatdata is in [here](conversion_metadata/).
4. Once the metadata has the specific details as you want, run the following commands
   ```
   cow_tool convert <file-path-csv>
   ```
5. run query to find objectID and related conxrefID
6. run [script](dataConversion/insert_links_conxrefs_to_objects.ipynb) to generate enriched triples with constituents and objects connections
7. run in prolog interface rdf_library:rdf_attach_library(<path-to-void.ttl-directory>).


 > NOW YOU HAVE ALL THE LINKED DATA UPLOADED TO CLIOPATRIA INTERFACE!!!


## Modelling Decisions:
### Objects

[Linkedart basic pattern](https://linked.art/model/base/)



Virtual column might not have a "name" or "id". 

```
Object a crm:E22_Human-Made_Object; 
    rdfs:label ObjectName; 
```

Types and Classification ignored   

Blank node is denoted as "virtual"

```
Title --> a a crm:E33_E41_Linguistic_Appellation;
        crm:P190_has_symbolic_content ... ;
        crm:P2_has_type <http://vocab.getty.edu/aat/300404670>
```

Medium --> made_of

ignored:
```
ObjectHeightCMOLD	ObjectWidthCMOLD	ObjectDepthCMOLD	ObjectDiameterCMOLD	ObjectWeightKGOLD field ignored     
```

we are not keeping objectID column, but objectID exists as @base+{objectID}

I did not mention linguistic tag with title

I did not mention linguistic tag with dimension

DateBegin	DateEnd Dated --> Considered production date

will ignore: 
- ObjectCount
- DepartmentID	
- LoanClassID
- CreditLine
- PublicAccess
- 'CuratorApproved', 'OnView', 'TextSearchID', 'LoginID', 'EnteredDate',
       'SysTimeStamp', 'Accountability', 'ObjectLevelID', 'ObjectTypeID',
       'ObjectScreenID', 'LoanClass', 'ObjectDiamCMOLD', 'IsVirtual',
       'IsTemplate', 'InJurisdiction', 'SearchObjectNumber'

```
TODO: ClassificationID	SubClassID	Type
TODO: Signed  Inscribed   Markings    Chat    Description   SortNumber
TODO: Exhibitions', 'Provenance', 'PubReferences', 'Notes'
```

### Actor/Constiteunts
[Actor Schema](https://linked.art/model/actor/)
- TODO: actor should have rdfs:label
- I am assuming all constituent f type: "crm:E21_Person"
- Ignored attribute:
  - Active
  - Institution	
  - LastSoundEx	
  - FirstSoundEx	
  - InstitutionSoundEx
  - N_DisplayName	
  - N_DisplayDate	
  - salutation	
  - Approved	
  - PublicAccess	
  - IsPrivate	
  - DefaultNameID	
  - SystemFlag	
  - InternalStatus	
  - DefaultDisplayBioID	
- AlphaSort --> considered primary name
- TODO: NameTitle
- TODO: CulturalGroup
- TODO: where I am going to state "DisplayDate"
- TODO: Nationality should have aat vocabulary; buyt omittied for the ease of current task


### Provenance activity

#### THROUGH OBJECT ACCESSION LOT


```
SELECT ?object ?accession ?status ?method ?time
            WHERE{
            ?object <https://pressingmatter.nl/Bronbeek/Objects/vocab/ObjectStatusID> [rdfs:label ?status].
            ?accession <https://pressingmatter.nl/Bronbeek/ObjAccession/vocab/ObjectID> ?object .
            ?accession <https://pressingmatter.nl/Bronbeek/ObjAccession/vocab/AccessionMethodID> [rdfs:label ?method] .
            OPTIONAL {?accession <https://pressingmatter.nl/Bronbeek/ObjAccession/vocab/AccessionISODate> ?time .}
            }
```

```
<www.example.com/Bronbeek/Provenance/1> a crm:E7_Activity ;
    rdfs:label " " ; #objectstatus
    crm:P2_has_type <http://vocab.getty.edu/aat/300055863> ;
    crm:P9_consists_of <www.example.com/Bronbeek/Acquisition/1> .

www.example.com/Bronbeek/Acquisition/1> a crm:E8_Acquisition ;
    crm:P4_time-span [crm:P82a_begin_of_the_begin 
                        crm:P82b_end_of_the_end ]; #accessionISODate
    rdfs:label " " ; #accessionmethod
    crm:P24_transferred_titled_of <https://example.com/Bronbeek/Objects/30966> .

<http://vocab.getty.edu/aat/300055863> a crm:E55_Type ;
    rdfs:label "Provenance Activity" .
```

> Remarks: we olso have object status or accession method "onbekend" / stolen; But, ignored in the conversion and considered everything as acquision, keeping the corresponding rdfs:label "object status"(provenance activity) and "acqusition method"(acquisition event)

#### THROUGH CONSTITUENTS
Get all the constitients and objects where the roletypeID=2;
 
1. SPAQRL query
```
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>

SELECT ?event ?constituent ?object
WHERE{
    ?conxrefdetailID <https://example.com/ConXrefDetails/vocab/ConstituentID> ?constituent .
  	?conxrefdetailID <https://example.com/ConXrefDetails/vocab/Prefix> ?event .
  	?conxrefdetailID <https://example.com/ConXrefDetails/vocab/RoleTypeID> ?RoleTypeID .
    ?conxrefdetailID <https://example.com/ConXrefDetails/vocab/ConXrefID> ?conxrefID .
  	?conxrefID skos:related ?object .
    FILTER (?RoleTypeID = <https://example.com/RoleTypes/2>).
}
```
2.  For each row [add](insert_links_conxrefs_to_objects.ipynb) an provenance activity that consists of an acqusistion 

```
<www.example.com/Bronbeek/Provenance/1> a crm:E7_Activity ; 
    crm:P14_carried_out_by <https://example.com/Bronbeek/Constituents/2658> ; #constituents
    crm:P2_has_type <http://vocab.getty.edu/aat/300055863> ;
    crm:P9_consists_of <www.example.com/Bronbeek/Acquisition/1> .

www.example.com/Bronbeek/Acquisition/1> a crm:E8_Acquisition ;
    crm:P4_timpe-span [crm:P82a_begin_of_the_begin 
                        rm:P82b_end_of_the_end ]; #accessionISODate
    rdfs:label " " ; #accessionmethod
    crm:P23_transferred_titled_from <https://example.com/Bronbeek/Constituents/2658> ;
    crm:P24_transferred_titled_of <https://example.com/Bronbeek/Objects/30966> .

<http://vocab.getty.edu/aat/300055863> a crm:E55_Type ;
    rdfs:label "Provenance Activity" .
```

### Former owner

- RoleType ID = 5(vroegere eigenaar or former owner) lists all the previous owner of an object 

```
   <object> crm:P51_has_former_or_current_owner <constituent>
```

### Person related to object
- RoleType ID = 1 lists person related to object, for example, person photographed or depicted, data subject, from drawing by
- I am also deleting previously created triples as `conxref_to_object.ttl` as I added all the RoleTypeID=1 2 and 5 seperately.
```
  <object> skos:related <constituent>
```

#### Remarks
> - RoleTypes = 1, 2, 5 are connected with objects
> - RoleTypeID = 4 is not interesting
>  - RoleTypeID 9(Gebeurtenis gerelateerd) and 11(Media Related/ Gerelateerde persoon/instelling) could be interesting

| RoleTypeID | Roletype               | Translated          |                                                                                                                                                                                                                                                                                             |
| ---------- | ---------------------- | ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1          | Objecten gerelateerd   | Objects related     | This type has different roles;<br>RoleID (19, 21, 24, 28, 30, 65, 71, 72, 73) --> can best be described as object related to this `actor` <br>RoleID: 21 = new owner <br>RoleID: 29 = collector #todo not sure how to portray it<br>RoleID: 31 = borrower  #todo not sure how to portray it |
| 2          | Verwerving gerelateerd | Acquisition Related | RoleID specify specific type of acquisition                                                                                                                                                                                                                                                 |
| 5          | Pedigree gerelateerd   | Pedigree Related    | RoleID = 5; vroegere eigenaar or former owner                                                                                                                                                                                                                                               |



# Concerns:
- can I use type crm:E22_Human-Made_Object for all objects? 
- if some input is NULL, I still end up adding a intermidiatry node or blank node for it. How do I get rid of it?
- Do I consider "medium" as material or shall I consider this field as linguistic description as example given in Linkedart. 
    ```
        @prefix crm: <http://www.cidoc-crm.org/cidoc-crm/> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

        <https://linked.art/example/object/27> a crm:E22_Human-Made_Object ;
            rdfs:label "Painting on Canvas" ;
            crm:P67i_is_referred_to_by [ a crm:E33_Linguistic_Object ;
                    crm:P190_has_symbolic_content "Oil on Canvas" ;
                    crm:P2_has_type <http://vocab.getty.edu/aat/300435429> ;
                    crm:P72_has_language <http://vocab.getty.edu/aat/300388277> ] .

        <http://vocab.getty.edu/aat/300388277> a crm:E56_Language ;
            rdfs:label "English" .

        <http://vocab.getty.edu/aat/300418049> a crm:E55_Type ;
            rdfs:label "Brief Text" .

        <http://vocab.getty.edu/aat/300435429> a crm:E55_Type ;
            rdfs:label "Material Statement" ;
            crm:P2_has_type <http://vocab.getty.edu/aat/300418049> .
    ```
- According to Linkedart, I should use la:equivalent to link person, not owl:sameAs
- I added crm:P51_has_former_or_current_owner based on RoleTypeID=5, where the text is "oorspronkelijk bezit van" or "original property of"



# TRY OUT QUERIES

```
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT (COUNT(DISTINCT(?conxrefdetailID)) AS ?n)
 WHERE{
  ?conxrefdetailID <https://pressingmatter.nl/Bronbeek/ConXrefDetails/vocab/ConstituentID> ?constituent .
  ?conxrefdetailID <https://pressingmatter.nl/Bronbeek/ConXrefDetails/vocab/Prefix> ?event .
  ?conxrefdetailID <https://pressingmatter.nl/Bronbeek/ConXrefDetails/vocab/ConXrefID> ?conXref .
  ?conXref <https://pressingmatter.nl/Bronbeek/ConXrefs/vocab/ID> ?ID .
  ?conXref <https://pressingmatter.nl/Bronbeek/ConXrefs/vocab/TableID> ?TableID .
  ?object <https://pressingmatter.nl/Bronbeek/Objects/vocab/ObjectID> ?ID .
  ?object <https://pressingmatter.nl/Bronbeek/Objects/vocab/ObjectStatusID> <https://pressingmatter.nl/Bronbeek/ObjectStatuses/1> .
}LIMIT 10
```

276968

```
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT (COUNT(DISTINCT(?conxrefdetailID)) AS ?n)
 WHERE{
  ?conxrefdetailID <https://pressingmatter.nl/Bronbeek/ConXrefDetails/vocab/ConstituentID> ?constituent .
  ?conxrefdetailID <https://pressingmatter.nl/Bronbeek/ConXrefDetails/vocab/Prefix> ?event .
  ?conxrefdetailID <https://pressingmatter.nl/Bronbeek/ConXrefDetails/vocab/ConXrefID> ?conXref .
  ?conXref <https://pressingmatter.nl/Bronbeek/ConXrefs/vocab/ID> ?ID .
  ?conXref <https://pressingmatter.nl/Bronbeek/ConXrefs/vocab/TableID> ?TableID .
  ?object <https://pressingmatter.nl/Bronbeek/Objects/vocab/ObjectID> ?ID .
}LIMIT 10
```

290196

```
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT (COUNT(DISTINCT(?conxrefdetailID)) AS ?n)
 WHERE{
  ?conxrefdetailID <https://pressingmatter.nl/Bronbeek/ConXrefDetails/vocab/ConstituentID> ?constituent .
  ?conxrefdetailID <https://pressingmatter.nl/Bronbeek/ConXrefDetails/vocab/Prefix> ?event .
  ?conxrefdetailID <https://pressingmatter.nl/Bronbeek/ConXrefDetails/vocab/ConXrefID> ?conXref .
  ?conXref <https://pressingmatter.nl/Bronbeek/ConXrefs/vocab/ID> ?ID .
  ?conXref <https://pressingmatter.nl/Bronbeek/ConXrefs/vocab/TableID> ?TableID .
  FILTER (?TableID = "108"^^<https://pressingmatter.nl/Bronbeek/ConXrefs/interger>) .
  ?conXref <https://pressingmatter.nl/Bronbeek/ConXrefs/vocab/RoleTypeID> <https://pressingmatter.nl/Bronbeek/RoleTypes/2> .
  ?object <https://pressingmatter.nl/Bronbeek/Objects/vocab/ObjectID> ?ID .
}LIMIT 10
```

182042

```
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT (COUNT(DISTINCT(?conxrefdetailID)) AS ?n)
 WHERE{
  ?conxrefdetailID <https://pressingmatter.nl/Bronbeek/ConXrefDetails/vocab/ConstituentID> ?constituent .
  ?conxrefdetailID <https://pressingmatter.nl/Bronbeek/ConXrefDetails/vocab/Prefix> ?event .
  ?conxrefdetailID <https://pressingmatter.nl/Bronbeek/ConXrefDetails/vocab/ConXrefID> ?conXref .
  ?conXref <https://pressingmatter.nl/Bronbeek/ConXrefs/vocab/ID> ?ID .
  ?conXref <https://pressingmatter.nl/Bronbeek/ConXrefs/vocab/TableID> ?TableID .
  FILTER (?TableID = "108"^^<https://pressingmatter.nl/Bronbeek/ConXrefs/interger>) .
  ?conXref <https://pressingmatter.nl/Bronbeek/ConXrefs/vocab/RoleTypeID> <https://pressingmatter.nl/Bronbeek/RoleTypes/2> .
  ?object <https://pressingmatter.nl/Bronbeek/Objects/vocab/ObjectID> ?ID .
  ?accession <https://pressingmatter.nl/Bronbeek/ObjAccession/vocab/ObjectID> ?object .
}LIMIT 10
```

182042

> so every conxrefdetailID has corresponding acqusiiton

```
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT (COUNT(DISTINCT(?conxrefdetailID)) AS ?n)
 WHERE{
  ?conxrefdetailID <https://pressingmatter.nl/Bronbeek/ConXrefDetails/vocab/ConstituentID> ?constituent .
  ?conxrefdetailID <https://pressingmatter.nl/Bronbeek/ConXrefDetails/vocab/Prefix> ?event .
  ?conxrefdetailID <https://pressingmatter.nl/Bronbeek/ConXrefDetails/vocab/ConXrefID> ?conXref .
  ?conXref <https://pressingmatter.nl/Bronbeek/ConXrefs/vocab/ID> ?ID .
  ?conXref <https://pressingmatter.nl/Bronbeek/ConXrefs/vocab/TableID> ?TableID .
  FILTER (?TableID = "108"^^<https://pressingmatter.nl/Bronbeek/ConXrefs/interger>) .
  ?conXref <https://pressingmatter.nl/Bronbeek/ConXrefs/vocab/RoleTypeID> <https://pressingmatter.nl/Bronbeek/RoleTypes/2> .
  ?object <https://pressingmatter.nl/Bronbeek/Objects/vocab/ObjectID> ?ID .
  ?object <https://pressingmatter.nl/Bronbeek/Objects/vocab/ObjectStatusID> <https://pressingmatter.nl/Bronbeek/ObjectStatuses/1> .
}LIMIT 10
```

178270

```
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT (COUNT(DISTINCT(?conxrefdetailID)) AS ?n)
 WHERE{
  ?conxrefdetailID <https://pressingmatter.nl/Bronbeek/ConXrefDetails/vocab/ConstituentID> ?constituent .
  ?conxrefdetailID <https://pressingmatter.nl/Bronbeek/ConXrefDetails/vocab/Prefix> ?event .
  ?conxrefdetailID <https://pressingmatter.nl/Bronbeek/ConXrefDetails/vocab/ConXrefID> ?conXref .
  ?conXref <https://pressingmatter.nl/Bronbeek/ConXrefs/vocab/ID> ?ID .
  ?conXref <https://pressingmatter.nl/Bronbeek/ConXrefs/vocab/TableID> ?TableID .
  FILTER (?TableID = "108"^^<https://pressingmatter.nl/Bronbeek/ConXrefs/interger>) .
  ?conXref <https://pressingmatter.nl/Bronbeek/ConXrefs/vocab/RoleTypeID> <https://pressingmatter.nl/Bronbeek/RoleTypes/2> .
  ?object <https://pressingmatter.nl/Bronbeek/Objects/vocab/ObjectID> ?ID .
  ?object <https://pressingmatter.nl/Bronbeek/Objects/vocab/ObjectStatusID> <https://pressingmatter.nl/Bronbeek/ObjectStatuses/3> .
}LIMIT 10
```
