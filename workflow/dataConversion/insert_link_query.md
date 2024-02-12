###### Quuery to insert skos:related links among object and conxref

- in practice, instead of "CONSTRUCT" I used "SELECT" and then used the [script](insert_links_conxrefs_to_objects.ipynb) to generate graph.
-  
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

https://example.com/Bronbeek/Objects/10000