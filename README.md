# databat-kgc-knxproj

Knowledge Graph construction from a ETS5 project file ( `.knxproj` )

The scripts in this repository are used to generate a knowledge graph with entry point https://ci.mines-stetienne.fr/knx 

This knowledge publicly documents the historical KNX configuration of Espace Fauriel Building at Mines Saint-Étienne using the Thing Description ontology. 

## How to run

run the following commands, with the appropriate dependencies.

```
python3 -m pip install rdflib
python3 list_devices_td.py
python3 storeTurtleFiles.py
```
