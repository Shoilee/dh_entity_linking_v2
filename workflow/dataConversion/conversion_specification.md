# Remarks:
cow-csvw basic propeties:


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
- ObjectStatusID
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
- 