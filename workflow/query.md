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