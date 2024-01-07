###### Quuery to insert owl:sameAS links
```SPARQL
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

CONSTRUCT {?s skos:related ?object}
WHERE{
  Graph <https://example.com/ConXrefs/ConXrefs/assertion/d8c707c2/2024-01-07T17:23>{
    ?s <https://example.com/ConXrefs/vocab/ID> ?ID .
    ?s <https://example.com/ConXrefs/vocab/TableID> ?TableID .
    ?s <https://example.com/ConXrefs/vocab/TableID> ?TableID .
    {?s <https://example.com/ConXrefs/vocab/RoleTypeID> <https://example.com/RoleTypes/1>}
    UNION {?s <https://example.com/ConXrefs/vocab/RoleTypeID> <https://example.com/RoleTypes/2>} 
    UNION {?s <https://example.com/ConXrefs/vocab/RoleTypeID> <https://example.com/RoleTypes/5>} .
  }
  Graph <https://example.com/Objects/Objects/assertion/bad21d24/2024-01-07T20:54>{
    ?object <https://example.com/Objects/vocab/ObjectID> ?ID .
  }
}
```