# Remarks:

Object a crm:E22_Human-Made_Object; 
    rdfs:label ObjectName; 

Types and Classification ignored   

Blank node is denoted as "virtual"

Title --> a a crm:E33_E41_Linguistic_Appellation;
        crm:P190_has_symbolic_content ... ;
        crm:P2_has_type <http://vocab.getty.edu/aat/300404670>

Medium --> made_of

ObjectHeightCMOLD	ObjectWidthCMOLD	ObjectDepthCMOLD	ObjectDiameterCMOLD	ObjectWeightKGOLD field ignored     

we are not keeping objectID column, but objectID exists as @base+{objectID}

I did not mention linguistic tag with title

will ignore: 
- ObjectCount
- DepartmentID	
- ObjectStatusID
- LoanClassID
- CreditLine
- PublicAccess
- 
       'CuratorApproved', 'OnView', 'TextSearchID', 'LoginID', 'EnteredDate',
       'SysTimeStamp', 'Accountability', 'ObjectLevelID', 'ObjectTypeID',
       'ObjectScreenID', 'LoanClass', 'ObjectDiamCMOLD', 'IsVirtual',
       'IsTemplate', 'InJurisdiction', 'SearchObjectNumber'
       'Signed' --> NULL
       'Inscribed' --> only 2 row have valid value
       'Markings' --> only 1 row have valid value
  

TODO: ClassificationID	SubClassID	Type
TODO: DateBegin	DateEnd Dated
TODO: Dimensions    Signed  Inscribed   Markings    Chat    Description
TODO: Exhibitions', 'Provenance', 'PubReferences', 'Notes',
TODO: SortNumber

# Concerns:
- can I use type crm:E22_Human-Made_Object for all objects? 
- if some input is NULL, I still end up adding a intermidiatry node or blank node for it.