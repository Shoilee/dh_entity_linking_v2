# CQ-1a

1.  Is there any person involved in the provenance of this object with colonial background? 

> How many actor has military background?

```
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT (COUNT(DISTINCT ?nmvw_actor) AS ?n) 
WHERE{
 ?nmvw_object  a crm:E22_Human-Made_Object .
  #acquisition event
  {?nmvw_acq crm:P24_transferred_title_of ?nmvw_object .
   ?nmvw_acq crm:P23_transferred_title_from ?nmvw_actor .}
  UNION
  #production event
  {
    ?nmvw_object crm:P108i_was_produced_by ?nmvw_prod .
    ?nmvw_prod crm:P14_carried_out_by ?nmvw_actor .
  }
  UNION
  {
    ?nmvw_object crm:P52_has_current_owner ?nmvw_actor .
  }
  UNION
  {
    ?nmvw_object crm:P51_has_former_or_current_owner ?nmvw_actor .
  }
  
  ?nmvw_actor owl:sameAs ?bronbeek_actor .
}
```

> How many object may have military connection? 
```
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT (COUNT(DISTINCT ?nmvw_object) AS ?n)
WHERE{
 ?nmvw_object  a crm:E22_Human-Made_Object .
  #acquisition event
  {
    ?nmvw_acq crm:P24_transferred_title_of ?nmvw_object .
    ?nmvw_acq crm:P23_transferred_title_from ?nmvw_actor .
   }
  UNION
  #production event
  {
    ?nmvw_object crm:P108i_was_produced_by ?nmvw_prod .
    ?nmvw_prod crm:P14_carried_out_by ?nmvw_actor .
  }
  UNION
  {
    ?nmvw_object crm:P52_has_current_owner ?nmvw_actor .
  }
  UNION
  {
    ?nmvw_object crm:P51_has_former_or_current_owner ?nmvw_actor .
  }
  
  ?nmvw_actor owl:sameAs ?bronbeek_actor .
}GROUP BY ?nmvw_actor
```
   
# CQ-1b
1.  Is there a possible relation between objects that are linked to a same person?      

> Remarks: we considered production as part of provenance and we also considered person related to object as part of production.

```SPARQL
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT (COUNT(DISTINCT ?nmvw_object) AS ?n_nmvw_object)  ?nmvw_actor (COUNT(DISTINCT ?bronbeek_object) AS ?n_bronbeek_object) 
WHERE{
 ?nmvw_object  a crm:E22_Human-Made_Object .
  #acquisition event
  {?nmvw_acq crm:P24_transferred_title_of ?nmvw_object .
   ?nmvw_acq crm:P23_transferred_title_from ?nmvw_actor .}
  UNION
  {
    ?nmvw_object crm:P108i_was_produced_by ?nmvw_prod .
    ?nmvw_prod crm:P14_carried_out_by ?nmvw_actor .
  }
  
  ?nmvw_actor owl:sameAs ?bronbeek_actor .
  
  ?bronbeek_object  a crm:E22_Human-Made_Object .
  #acquisition event
  {
    ?bronbeek_acq crm:P24_transferred_title_of ?bronbeek_object .
    ?bronbeek_acq crm:P23_transferred_title_from ?bronbeek_actor . 
  }
  UNION
  # person related to object
  {
    ?bronbeek_object skos:related ?bronbeek_actor .
  }
  ?bronbeek_actor a crm:E21_Person .
  
} GROUP BY ?nmvw_actor
```

# CQ-2

2. Which objects are collected by person(s) with colonial history?
```
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT (COUNT(DISTINCT ?nmvw_object) AS ?n)
WHERE{
 ?nmvw_object  a crm:E22_Human-Made_Object .
  #acquisition event
  {
   ?nmvw_acq crm:P24_transferred_title_of ?nmvw_object .
   ?nmvw_acq crm:P23_transferred_title_from ?nmvw_actor .
  }
  UNION
  #production event
  {
    ?nmvw_object crm:P108i_was_produced_by ?nmvw_prod .
    ?nmvw_prod crm:P14_carried_out_by ?nmvw_actor .
  }
  UNION
  {
    ?nmvw_object crm:P52_has_current_owner ?nmvw_actor .
  }
  UNION
  {
    ?nmvw_object crm:P51_has_former_or_current_owner ?nmvw_actor .
  }
  
  ?nmvw_actor owl:sameAs ?bronbeek_actor .
}
```

# CQ-3
3,. Is there a relationship between person A and person B through object collection event?    
> inspiration link for `property path` SPARQL query: https://www.w3.org/TR/sparql11-property-paths/ 

```
PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX pm-bronbeek-vocab: <https://pressingmatter.nl/Bronbeek/Constituents/vocab/>
PREFIX owl: <http://www.w3.org/2002/07/owl#>

# connected through same event
SELECT * WHERE 
{
  ?p1 a crm:E39_Actor .
  ?p1 rdfs:label ?p1_name .
  ?p2 a crm:E21_Person . 
  ?p2 pm-bronbeek-vocab:DisplayName ?p2_name .
  ?event1 ?prop1 ?p3 .
  ?event1 ?prop2 ?p1 .
  ?p1 owl:sameAs ?p2.
  FILTER (?p1 != ?p3) .
  ?p3 a crm:E39_Actor .
  OPTIONAL {?p3 rdfs:label ?p3_name}.
} 
```