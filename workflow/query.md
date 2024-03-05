[Data Structure](https://drive.google.com/file/d/1YhG0_KXMwGstgzbmn68X8aBC6DKt0KSS/view?usp=sharing)

# CQ-1a

1.  Is there any person involved in the provenance of this object with colonial background? 
   ```
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT *
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

> How many actor has military background?

```
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT (COUNT(DISTINCT ?nmvw_actor) AS ?n) 
WHERE{
  Graph <https://pressingmatter.nl/NMVW/ccrdfobj.ttl>{
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
  }
  
  ?nmvw_actor owl:sameAs ?bronbeek_actor .
}
```

> How many object may have military connection? 
```
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT (COUNT(DISTINCT ?nmvw_object) AS ?n) ?nmvw_actor
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
LIMIT 10
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

> alternate query
```


PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT (COUNT(DISTINCT ?nmvw_object) AS ?n_nmvw_object)  ?nmvw_actor (COUNT(DISTINCT ?bb_object) AS ?n_bb_object) 
WHERE{
  GRAPH <https://pressingmatter.nl/NMVW/ccrdfobj.ttl>{
    ?nmvw_object  a crm:E22_Human-Made_Object .
  
    {?nmvw_acq crm:P24_transferred_title_of ?nmvw_object .
     ?nmvw_acq crm:P23_transferred_title_from ?nmvw_actor .}
    UNION
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
  }
  
  ?nmvw_actor owl:sameAs ?bb_actor .
  
GRAPH <https://pressingmatter.nl/Bronbeek/Objects/Objects/assertion/bad21d24/2024-03-01T12:54>{
    ?bb_object a crm:E22_Human-Made_Object .
    }
    #acquisition event
    {
      ?bb_acq crm:P24_transferred_title_of ?bb_object .
      ?bb_acq crm:P23_transferred_title_from ?bb_actor . 
    }
  UNION
    {
    ?bb_object crm:P108i_was_produced_by ?bb_prod .
    ?bb_prod crm:P14_carried_out_by ?bb_actor. 
    }
  UNION
    {
      	?bb_object crm:P52_has_current_owner ?bb_actor .
    }
  UNION
    {
      	?bb_object crm:P51_has_former_or_current_owner ?bb_actor .
    }
} GROUP BY ?nmvw_actor
```
> see calculation [results.ipynb](results.ipynb)

# CQ-2

2. Which objects are collected by person(s) with colonial history?
```
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT (COUNT(DISTINCT ?nmvw_object) AS ?n)
WHERE{
  Graph <https://pressingmatter.nl/NMVW/ccrdfobj.ttl>{
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
  }
  ?nmvw_actor owl:sameAs ?bronbeek_actor .
}
```

object per person

```
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT (COUNT(DISTINCT ?nmvw_object) AS ?n) ?nmvw_actor ?nmvw_actor_name 
WHERE{
  Graph <https://pressingmatter.nl/NMVW/ccrdfobj.ttl>{
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
  }
  ?nmvw_actor owl:sameAs ?bronbeek_actor .
  GRAPH <https://pressingmatter.nl/NMVW/ccrdfobj.ttl>{
    ?nmvw_actor rdfs:label ?nmvw_actor_name .}
} GROUP BY ?nmvw_actor
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

# CQ-4
Which objects were collected in this geographical location? 

> E8_Acqusition do not have P7_took_place_at for both NMVW and Bronbeek .
```
# TODO: if you query acqusition event for place, we get zero matches.
```
> But, if we encorporate production and take that place into account, we get some results back
```
  PREFIX owl: <http://www.w3.org/2002/07/owl#>
  PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
  PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
  PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

  SELECT *
  WHERE{
    GRAPH <https://pressingmatter.nl/NMVW/ccrdfobjacquisition_15_names.ttl>{
      ?nmvw_prod crm:P7_took_place_at ?nmvw_prod_place.
      ?nmvw_prod_place a crm:E53_Place. 
      ?nmvw_obj crm:P108i_was_produced_by ?nmvw_prod .
      ?nmvw_obj a crm:E22_Human-Made_Object. 
      ?nmvw_acq crm:P24_transferred_title_of ?nmvw_obj .
      
      #acquisition event
      {?nmvw_acq crm:P23_transferred_title_from ?nmvw_actor .}
      UNION
      #production event
      {
        ?nmvw_obj crm:P108i_was_produced_by ?nmvw_prod .
        ?nmvw_prod crm:P14_carried_out_by ?nmvw_actor .
      }
      UNION
      {
        ?nmvw_obj crm:P52_has_current_owner ?nmvw_actor .
      }
      UNION
      {
        ?nmvw_obj crm:P51_has_former_or_current_owner ?nmvw_actor .
      }
    }
    ?nmvw_actor owl:sameAs ?bronbeek_actor .
  }
```

```
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT *
WHERE{
  GRAPH <https://pressingmatter.nl/Bronbeek/Objects/Objects/assertion/bad21d24/2024-03-01T12:54>{
    OPTIONAL {?bb_prod crm:P7_took_place_at ?bb_prod_place.
    ?bb_prod_place a crm:E53_Place. }
    ?bb_obj crm:P108i_was_produced_by ?bb_prod .
    ?bb_obj a crm:E22_Human-Made_Object. 
    ?bb_acq crm:P24_transferred_title_of ?bb_obj .
    
    #acquisition event
    {?bb_acq crm:P23_transferred_title_from ?bb_actor .}
    UNION
    #production event
    {
      ?nmvw_obj crm:P108i_was_produced_by ?nmvw_prod .
      ?bb_prod crm:P14_carried_out_by ?nmvw_actor .
    }
    UNION
    {
      ?bb_obj crm:P52_has_current_owner ?bb_actor .
    }
    UNION
    {
      ?bb_obj crm:P51_has_former_or_current_owner ?bb_actor .
    }
  }
  ?nmvw_actor owl:sameAs ?bb_actor .
}
```

> TODO: shall we consider culture as origin of production?
> Bronbeek production do not have an actor

> Bronbeek object do not have production place; but we can consider ``culture'' as P7_took_place for E12_Production event.
> So, the count now is 0. 
```
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT (COUNT(DISTINCT (?bb_obj)) AS ?n)
WHERE{
  GRAPH <https://pressingmatter.nl/Bronbeek/Objects/Objects/assertion/bad21d24/2024-03-01T12:54>{
    OPTIONAL {?bb_prod crm:P7_took_place_at ?bb_prod_place.
      ?bb_prod_place a crm:E53_Place. }
    ?bb_obj crm:P108i_was_produced_by ?bb_prod .
    ?bb_obj a crm:E22_Human-Made_Object. 
    }
  	?bb_acq crm:P24_transferred_title_of ?bb_obj .
  
  #acquisition event
    {
    	?bb_acq crm:P23_transferred_title_from ?bb_actor .	
  	}
    UNION
    {
      	?bb_obj crm:P52_has_current_owner ?bb_actor .
    }
    UNION
    {
      	?bb_obj crm:P51_has_former_or_current_owner ?bb_actor .
    }
  
  	?nmvw_actor owl:sameAs ?bb_actor

  
} LIMIT 10
```

> complete query
```
TODO: run on complete graph should work
```
> they both have only skos related connections to objects
>
https://hdl.handle.net/20.500.11840/pi57757 --> pm::Bronbeek/Constituents/7329  
https://hdl.handle.net/20.500.11840/pi64129 --> https://pressingmatter.nl/Bronbeek/Constituents/5995

```
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT (COUNT(DISTINCT (?bb_obj)) AS ?n)
WHERE{
  GRAPH <https://pressingmatter.nl/Bronbeek/Objects/Objects/assertion/bad21d24/2024-03-01T12:54>{
    OPTIONAL {?bb_prod crm:P7_took_place_at ?bb_prod_place.
      ?bb_prod_place a crm:E53_Place. }
    ?bb_obj crm:P108i_was_produced_by ?bb_prod .
    ?bb_obj a crm:E22_Human-Made_Object. 
    }
  	?bb_acq crm:P24_transferred_title_of ?bb_obj .
  
  #acquisition event
    {
    	?bb_acq crm:P23_transferred_title_from ?bb_actor .	
  	}
    UNION
    {
      	?bb_obj crm:P52_has_current_owner ?bb_actor .
    }
    UNION
    {
      	?bb_obj crm:P51_has_former_or_current_owner ?bb_actor .
    }
  	?nmvw_actor owl:sameAs ?bb_actor

    GRAPH <https://pressingmatter.nl/NMVW/ccrdfobjacquisition_15_names.ttl>{
      ?nmvw_prod crm:P7_took_place_at ?nmvw_prod_place.
      ?nmvw_prod_place a crm:E53_Place. 
      ?nmvw_obj crm:P108i_was_produced_by ?nmvw_prod .
      ?nmvw_obj a crm:E22_Human-Made_Object. 
      ?nmvw_acq crm:P24_transferred_title_of ?nmvw_obj .
      
      #acquisition event
      {?nmvw_acq crm:P23_transferred_title_from ?nmvw_actor .}
      UNION
      #production event
      {
        ?nmvw_obj crm:P108i_was_produced_by ?nmvw_prod .
        ?nmvw_prod crm:P14_carried_out_by ?nmvw_actor .
      }
      UNION
      {
        ?nmvw_obj crm:P52_has_current_owner ?nmvw_actor .
      }
      UNION
      {
        ?nmvw_obj crm:P51_has_former_or_current_owner ?nmvw_actor .
      }
    }
} 
```


# CQ-5
Which objects were collected during this historical  event? 

```
PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>

SELECT ?histevet_name ?histevet_btime ?histevet_etime ?nmvw_obj 
WHERE{
    GRAPH <https://pressingmatter.nl/NMVW/>{
    ?histevet crm:P140i_was_attributed_by ?o .
    ?histevet  crm:P1_is_identified_by ?title .
    ?histevet crm:P4_has_time-span [crm:P82a_begin_of_the_begin ?histevet_btime;
									crm:P82b_end_of_the_end ?histevet_etime] .
    ?title crm:P190_has_symbolic_content ?histevet_name .
    ?o a crm:E13_Attribute_Assignment .
    ?o crm:P141_assigned ?nmvw_obj .
    # ?nmvw_obj a crm:E22_Human-Made_Object .
  } 
}
```

> For Bronbeek, only If you can define the event with specific time and place? We do not need to put the historical events in the data for that. 

# CQ-6

Which objects were potentially collected in this geographical location during this time period from both dataset?  
```
SELECT ?obj ?place ?b_time ?e_time WHERE
{
  ?obj a crm:E24_Physical_Human-Made_Thing .
  ?activity crm:P9_consists_of ?sub .
  ?sub crm:P7_took_place_at ?place. 
  ?sub crm:P4_has_time-span ?time .
  ?time crm:P82a_begin_of_the_begin ?b_time .
  ?time crm:P82b_end_of_the_end ?e_time.
  ?activity crm:P24_transferred_title_of ?obj .
} 
```

# Validation data
https://book.validatingrdf.com/bookHtml011.html 
https://sphn-semantic-framework.readthedocs.io/en/latest/user_guide/data_quality.html 







