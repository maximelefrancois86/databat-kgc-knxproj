import sys
import os
from rdflib import Graph, RDF, Literal, BNode
from rdflib.term import Node
from app.namespaces import *
import shutil


g=Graph()
g.parse("temp/output.ttl")
print(f"total number of triples{len(g)}")

len(list(g.query("""SELECT * WHERE { ?x a td:Thing})


n = 0
sum = 0
for root, dirs, files in os.walk("public"):
    for file in files:
        if not file.endswith(".ttl"):
            continue
        g = Graph()
        g.parse(f"{root}/{file}")
        n +=1
        sum += len(g)
print(f"number of graphs {n}") 
print(f"total number of triples {sum}") 
print(f"average number of triples {sum/n}") 