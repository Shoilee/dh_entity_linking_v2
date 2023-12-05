### STEPS:

1. pip3 install cow-csvw

2. cow_tool build bronbeek_constituents.tsv --base 'https://example.com/bronbeek-constituents'

3. Change the metadata-json file →  "aboutUrl": "{ConstituentID}", from “aboutUrl”: “_row”
4. 
```
cow_tool convert bronbeek_constituents.tsv 
```

 
