### 1. Query to insert skos:related links among object and conxref

- in practice, instead of "CONSTRUCT" I used "SELECT" and then used the [script](insert_links_conxrefs_to_objects.ipynb) to generate graph.

```SPARQL
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

CONSTRUCT {?s skos:related ?object}
WHERE{
  Graph <https://example.com/ConXrefDetails/ConXrefDetails/assertion/c413cbfc/2024-02-12T06:55>{
    ?s <https://example.com/ConXrefs/vocab/ID> ?ID .
    ?s <https://example.com/ConXrefs/vocab/TableID> ?TableID .
    ?s <https://example.com/ConXrefs/vocab/TableID> ?TableID .
    {?s <https://example.com/ConXrefs/vocab/RoleTypeID> <https://example.com/RoleTypes/1>}
    UNION {?s <https://example.com/ConXrefs/vocab/RoleTypeID> <https://example.com/RoleTypes/2>} 
    UNION {?s <https://example.com/ConXrefs/vocab/RoleTypeID> <https://example.com/RoleTypes/5>} .
  }
  Graph <https://example.com/Bronbeek/Objects/Objects/assertion/bad21d24/2024-02-12T14:20>{
    ?object <https://example.com/Bronbeek/Objects/vocab/ObjectID> ?ID .
  }
}
```

### 2. query to find out which objects are connected through same person in both dataset

```SPARQL
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>

SELECT ?name ?constituentID ?conxrefdetailID ?conxrefID ?object_bronbeek ?nmvw_constituent ?event ?nmvw_object
WHERE{
    ?constituentID <https://example.com/Bronbeek/Constituents/vocab/DisplayName> ?name .
    ?conxrefdetailID <https://example.com/ConXrefDetails/vocab/ConstituentID> ?constituentID .
    ?conxrefdetailID <https://example.com/ConXrefDetails/vocab/ConXrefID> ?conxrefID .
  	?conxrefID skos:related ?object_bronbeek .
  	?nmvw_constituent owl:sameAs ?constituentID .
  	?event ?p ?nmvw_constituent .
  	?nmvw_object ?p1 ?event .
  	?nmvw_object a crm:E22_Human-Made_Object .
} LIMIT 100

```

### 3. query to see how constituents are linked with person only for acquisition event as RoleTRypeID == 2
```SPARQL
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>

SELECT ?constituentID ?event ?conxrefdetailID ?RoleTypeID ?role ?conxrefID ?object_bronbeek 
WHERE{
    ?conxrefdetailID <https://example.com/ConXrefDetails/vocab/ConstituentID> ?constituentID .
  	?conxrefdetailID <https://example.com/ConXrefDetails/vocab/Prefix> ?event .
  	?conxrefdetailID <https://example.com/ConXrefDetails/vocab/RoleTypeID> ?RoleTypeID .
    ?conxrefdetailID <https://example.com/ConXrefDetails/vocab/ConXrefID> ?conxrefID .
  	?conxrefID <https://example.com/ConXrefs/vocab/RoleID> ?RoleID .
  	?RoleID skos:prefLabel ?role .
  	?conxrefID skos:related ?object_bronbeek .
    FILTER (?RoleTypeID = <https://example.com/RoleTypes/2>).
}
```