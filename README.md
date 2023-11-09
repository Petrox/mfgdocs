# mfgdocs
Produce simple documentation for any manufacturing process.

The idea is to create a json/yaml storage format for version control that is then translated into graphviz for visualization.

This application contains a visual editor for the manufacturing steps and provides integration to manufacturing systems, but the output is a version controlled text based repository containing all the information necessary for manufacturing.

 - we keep a list of
 - Parts to build
 - BOM items
 - Tools
 - Machines
 - Activities / Actions (work)
 - Consumables (should be associated to tools and machines ideally)
 - Safety equipments (related to task)
 - Locations
 - 
 Then the user could associate these into a BuildStep:
 - input parts (*quantity)
 - input materials (*quantity)
 - consumables (*quantity)
 - tools (*quantity)
 - machines (*quantity)
 - textual description for each step, in markdown, with image uploads
 - output parts (*quantity)
 - other buildsteps this one starts after (+offset in hours)
 - setup and cooldown time (in hours)

 Then the forest of these buildsteps can be rendered using graphviz and any inputs and outputs connected, with color coded resourceusage.
 