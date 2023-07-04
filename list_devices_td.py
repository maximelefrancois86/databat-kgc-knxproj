#!/usr/bin/env python3
'''
This script analyses the contents of an extracted knxproj file and generates thing descriptions for the devices, including their configuration, and their operations
'''
import xml.etree.ElementTree as ET
from rdflib import Graph, URIRef, BNode, Literal, RDF, RDFS, OWL, SKOS, SSN, SOSA
from rdflib.namespace import Namespace, DefinedNamespace
from urllib.parse import quote
import csv
from collections import namedtuple
from app.namespaces import *

def decimalToIndividualAddress3(decimal):
    decimal = int(decimal)
    area = decimal >> 12
    line = decimal >> 8 & 15
    device = decimal & 255
    return f"{area}/{line}/{device}"

def decimalToGroupAddress3(decimal):
    decimal = int(decimal)
    main = decimal >> 11
    middle = decimal >> 8 & 7
    subgroup = decimal & 255
    return f"{main}/{middle}/{subgroup}"




#project = "2021_04_29_Espace_Fauriel_v20"
#project = "2022_01_11_Espace_Fauriel_v20"
#project = "../knxproj/2022_12_06_Espace_Fauriel_v20"

base = "https://ci.mines-stetienne.fr/knx/emse/fayol/"


graph = Graph(namespace_manager=namespaceManager)


def clean(value:str):
    if " °C" in value:
        return Literal(f"{value[:-3]} Cel", datatype=CDT.ucum)
    elif "°C" in value:
        return Literal(f"{value[:-2]} Cel", datatype=CDT.ucum)
    elif value.endswith(" mn"):
        return Literal(f"{value[:-3]} min", datatype=CDT.ucum)
    elif value.endswith(" mn "):
        return Literal(f"{value[:-4]} min", datatype=CDT.ucum)
    elif value.endswith(" min"):
        return Literal(value, datatype=CDT.ucum)
    elif value.endswith(" min"):
        return Literal(value, datatype=CDT.ucum)
    elif value.endswith(" h"):
        return Literal(value, datatype=CDT.ucum)
    elif value.endswith("  Milli secondes"):
        return Literal(f"{value[:-16]} ms", datatype=CDT.ucum)
    elif value.endswith("  ms"):
        return Literal(value, datatype=CDT.ucum)
    else:
        return Literal(value)        

def defineSchema(graph:Graph, HardwareName:str, Ox:str, co:URIRef):
    #HardwareName TF303,TL320B V1.2,TF305,TJ400,TB305,TA 300,TB300,TB301,STYA608,TK300,TB326,TL204B V3.0,TE300,TF312,TE302,TB330,TA301,TB344,TB345,TB350,TG300,TB309,TF300,
    if HardwareName == "TF303" or HardwareName == "TF305":
        if Ox == "O-0":
            graph.add((co, RDF.type, JS.NumberSchema))
        elif Ox == "O-4":
            graph.add((co, RDF.type, JS.BooleanSchema))
        elif Ox == "O-5":
            graph.add((co, RDF.type, JS.ObjectSchema))
        elif Ox == "O-6":
            graph.add((co, RDF.type, JS.ObjectSchema))
        elif Ox == "O-7":
            graph.add((co, RDF.type, JS.NumberSchema))
        elif Ox == "O-8":
            graph.add((co, RDF.type, JS.NumberSchema))
        elif Ox == "O-9":
            graph.add((co, RDF.type, JS.NumberSchema))
        elif Ox == "O-10":
            graph.add((co, RDF.type, JS.NumberSchema))
        elif Ox == "O-11":
            graph.add((co, RDF.type, JS.NumberSchema))
        elif Ox == "O-12":
            graph.add((co, RDF.type, JS.NumberSchema))
        elif Ox == "O-13":
            graph.add((co, RDF.type, JS.BooleanSchema))
    elif HardwareName == "TF312":
        if Ox == "O-0":
            graph.add((co, RDF.type, JS.NumberSchema))
        if Ox == "O-1":
            graph.add((co, RDF.type, JS.BooleanSchema))
        if Ox == "O-5":
            graph.add((co, RDF.type, JS.ObjectSchema))
        elif Ox == "O-6":
            graph.add((co, RDF.type, JS.ObjectSchema))
        elif Ox == "O-8":
            graph.add((co, RDF.type, JS.NumberSchema))
        elif Ox == "O-9":
            graph.add((co, RDF.type, JS.NumberSchema))
        elif Ox == "O-10":
            graph.add((co, RDF.type, JS.NumberSchema))
        elif Ox == "O-11":
            graph.add((co, RDF.type, JS.NumberSchema))
        elif Ox == "O-12":
            graph.add((co, RDF.type, JS.NumberSchema))
        elif Ox == "O-13":
            graph.add((co, RDF.type, JS.BooleanSchema))
    elif HardwareName == "TL320B V1.2":
        if Ox == "O-0":
            graph.add((co, RDF.type, JS.ObjectSchema))
        elif Ox == "O-8":
            graph.add((co, RDF.type, JS.NumberSchema))
        elif Ox == "O-10":
            graph.add((co, RDF.type, JS.NumberSchema))
        elif Ox == "O-12":
            graph.add((co, RDF.type, JS.BooleanSchema))
        elif Ox == "O-13":
            graph.add((co, RDF.type, JS.ObjectSchema))


def parse_knxproj(project:str, graph:Graph):
    
    system = URIRef("1/0/254")
    graph.add((system, RDF.type, TD.Thing))
    graph.add((system, RDF.type, SSN.System))
    graph.add((system, RDFS.label, Literal("KNX/IP Gateway")))
    
    tree = ET.parse(f'{project}/P-0DCD/0.xml')
    Hardwarefile = f'{project}/M-0009/Hardware.xml'
    Hardwaretree = ET.parse(Hardwarefile)
    for area in tree.findall(".//{http://knx.org/xml/project/20}Area"):
        a = area.attrib["Address"]
        a_uri = URIRef(f"{a}")
        a_label = area.attrib["Name"].replace("\r","").replace("\n","")
        graph.add((a_uri, RDF.type, COSWOT.KNXArea))
        graph.add((a_uri, RDFS.label, Literal(a_label)))
        graph.add((a_uri, SKOS.hiddenLabel, Literal(a)))
        for line in area.findall("./{http://knx.org/xml/project/20}Line"):
            l = line.attrib["Address"]
            l_uri = URIRef(f"{a}/{l}")
            graph.add((a_uri, COSWOT.hasKNXLine, l_uri))
            graph.add((l_uri, RDF.type, COSWOT.KNXLine))
            l_label = line.attrib["Name"].replace("\r","").replace("\n","")
            graph.add((l_uri, RDFS.label, Literal(l_label)))
            graph.add((l_uri, SKOS.hiddenLabel, Literal(f"{a}/{l}")))
            for deviceInstance in line.findall("./{http://knx.org/xml/project/20}DeviceInstance"):
                if "Address" not in deviceInstance.attrib.keys():
                    continue
                d = deviceInstance.attrib["Address"]
                d_uri = URIRef(f"{a}/{l}/{d}")
                graph.add((l_uri, COSWOT.hasKNXDevice, d_uri))
                graph.add((d_uri, RDF.type, COSWOT.Device))
                graph.add((d_uri, RDF.type, TD.Thing))
                graph.add((d_uri, SKOS.hiddenLabel, Literal(f"{a}/{l}/{d}")))

                description = deviceInstance.attrib["Description"].replace("\r","")
                graph.add((d_uri, RDFS.label, Literal(description)))

                # Obtain information about this hardware application program
                Hardware2ProgramRefId = deviceInstance.attrib["Hardware2ProgramRefId"]
                Hardware2Program = Hardwaretree.find(".//{http://knx.org/xml/project/20}Hardware2Program[@Id='"+Hardware2ProgramRefId+"']")
                HardwareDescription = Hardwaretree.find(".//{http://knx.org/xml/project/20}Hardware2Program[@Id='"+Hardware2ProgramRefId+"']/../..").attrib["Name"]
                HardwareRefId = Hardware2Program.find("./{http://knx.org/xml/project/20}ApplicationProgramRef").attrib["RefId"]
                hardwarefile = f'{project}/M-0009/{HardwareRefId}.xml'
                hardwaretree = ET.parse(hardwarefile)          
                ApplicationProgram = hardwaretree.find(".//{http://knx.org/xml/project/20}ApplicationProgram")
                if ApplicationProgram == None:
                    print("ApplicationProgram is none for " + HardwareRefId)
                    continue
                HardwareName = ApplicationProgram.attrib["Name"]
                graph.add((d_uri, SCHEMA.description, Literal(HardwareDescription)))
                graph.add((d_uri, SCHEMA.model, Literal(HardwareName)))

                decimal = int(a) << 11 | int(l) << 8 | int(d)
                hexa = hex(decimal)
                for parameterInstanceRef in deviceInstance.findall("./{http://knx.org/xml/project/20}ParameterInstanceRefs/{http://knx.org/xml/project/20}ParameterInstanceRef"):
                    RefId = parameterInstanceRef.attrib["RefId"] # exemple: M-0009_A-0009-40-2B44_P-17_R-17
                    Value = parameterInstanceRef.attrib["Value"] # exemple: 6456
                    ParameterRef = hardwaretree.find(".//{http://knx.org/xml/project/20}ParameterRef[@Id='" + RefId +"']")
                    ParameterRefRefId = ParameterRef.attrib["RefId"] # exemple: M-0009_A-0009-40-2B44_P-1
                    Parameter = hardwaretree.find(".//{http://knx.org/xml/project/20}Parameter[@Id='" + ParameterRefRefId +"']")
                    ParameterName = Parameter.attrib["Name"].replace("\r","")
                    ParameterText = Parameter.attrib["Text"].replace("\r","")
                    ParameterType = Parameter.attrib["ParameterType"].replace("\r","")
                    Parameter = hardwaretree.find(".//{http://knx.org/xml/project/20}ParameterType[@Id='" + ParameterType +"']//{http://knx.org/xml/project/20}Enumeration[@Value='"+Value+"']")
                    if Parameter == None:
                        print("No Parameter for .//{http://knx.org/xml/project/20}ParameterType[@Id='" + ParameterType +"']//{http://knx.org/xml/project/20}Enumeration[@Value='"+Value+"']")
                        continue;
                    ParameterValueText = Parameter.attrib["Text"].replace("\r","")
                    p = URIRef(f"{a}/{l}/{d}#{quote(ParameterName)}")
                    graph.add((d_uri, TD.hasPropertyAffordance, p))
                    graph.add((p, RDF.type, TD.PropertyAffordance))
                    graph.add((p, TD.title, Literal(ParameterName)))
                    graph.add((p, TD.description, Literal(ParameterText)))
                    graph.add((p, TD.isObservable, Literal(False)))
                    graph.add((p, COSWOT.hasStableValue, clean(ParameterValueText)))


                for comObjectInstanceRef in deviceInstance.findall("./{http://knx.org/xml/project/20}ComObjectInstanceRefs/{http://knx.org/xml/project/20}ComObjectInstanceRef"):
                    comObjectInstanceRefRefId = comObjectInstanceRef.attrib["RefId"]
                    Ox = comObjectInstanceRefRefId[:comObjectInstanceRefRefId.find("_")]
                    co_uri = URIRef(f"{a}/{l}/{d}#{Ox}")
                    ## TODO: depending on HardwareName and Ox, the Schema may be known.
                    defineSchema(graph, HardwareName, Ox, co_uri)
                    if "Description" in comObjectInstanceRef.attrib:
                        graph.add((co_uri, RDFS.comment, Literal(comObjectInstanceRef.attrib["Description"])))
                    ComObject = hardwaretree.find(f".//{{http://knx.org/xml/project/20}}ComObject[@Id='{HardwareRefId}_{Ox}']")
                    graph.add((d_uri, TD.hasPropertyAffordance, co_uri))
                    graph.add((co_uri, RDF.type, TD.PropertyAffordance))
                    graph.add((co_uri, TD.title, Literal(Ox)))
                    graph.add((co_uri, RDFS.label, Literal(ComObject.attrib["Name"])))
                    graph.add((co_uri, TD.description, Literal(ComObject.attrib["FunctionText"])))
                    graph.add((co_uri, COSWOT.objectSize, Literal(ComObject.attrib["ObjectSize"])))

                    if "Links" not in comObjectInstanceRef.attrib.keys():
                        continue
                    for Link in comObjectInstanceRef.attrib["Links"].split(" "):
                        LinkId = "P-0DCD-0_" + Link
                        GroupAddress = tree.find(".//{http://knx.org/xml/project/20}GroupAddress[@Id='"+LinkId+"']")
                        address = GroupAddress.attrib["Address"]
                        
                        ga = URIRef(f"ga/{decimalToGroupAddress3(address)}")
                        graph.add((system, TD.hasPropertyAffordance, ga))
                        graph.add((ga, RDF.type, COSWOT.KNXGroupAddress))
                        graph.add((ga, RDF.type, TD.PropertyAffordance))
                        graph.add((co_uri, COSWOT.sharesFormsWith, ga))
                        graph.add((ga, COSWOT.sharesFormsWith, co_uri))
                        graph.add((ga, RDFS.label, Literal(GroupAddress.attrib["Name"])))
                        graph.add((ga, SKOS.hiddenLabel, Literal(decimalToGroupAddress3(address))))
                        
                        knxForm = BNode("ga" + decimalToGroupAddress3(address))
                        graph.add((ga, TD.hasForm, knxForm))
                        graph.add((knxForm, COSWOT.KNXMethodName, Literal("read")))
                        graph.add((knxForm, HCTL.hasOperationType, TD.readProperty))
                        graph.add((knxForm, HCTL.hasTarget, URIRef(f"knxip://195.83.140.67:3761/{decimalToGroupAddress3(address)}")))


def parse_source_devices(file, graph):
    system = URIRef("1/0/254")
    visited = set()
    with open(file, encoding='utf-8-sig') as csvfile:
        reader = csv.reader(csvfile, delimiter=";")
        columns = list(next(reader))
        for row in reader:
            data = { columns[i]: row[i] for i in range(len(columns))}
            ga = URIRef(f"ga/{data['Address']}")
            topic = data["topic"]
            if "temperature" not in topic:
                continue
            if "comfort" in topic:
                continue
            if "outside" in topic and "1ET/100" not in topic:
                continue
            if (ga, topic) in visited:
                continue
            visited.add((ga, topic))
            
            mqttForm = BNode(ga+"mqtt")
            graph.add((ga, TD.hasForm, mqttForm))
            graph.add((mqttForm, HCTL.forContentType, Literal("text/plain")))
            graph.add((mqttForm, HCTL.hasOperationType, TD.observeProperty))
            graph.add((mqttForm, MQV.controlPacket, Literal("subscribe")))
            graph.add((mqttForm, MQV.filter, Literal(topic)))
            graph.add((mqttForm, HCTL.hasTarget, URIRef(f"mqtt://193.49.165.40:1883")))

            ga_history = URIRef(f"ga/{data['Address']}#history")
            graph.add((ga_history, RDF.type, TD.PropertyAffordance))
            graph.add((system, TD.hasPropertyAffordance, ga_history))
            graph.add((ga_history, RDF.type, JS.ArraySchema))
            bnitems = BNode()
            graph.add((ga_history, JS.items, bnitems))
            graph.add((bnitems, RDF.type, JS.ObjectSchema))
            bnitemsp1 = BNode()
            graph.add((bnitems, JS.properties, bnitemsp1))
            graph.add((bnitemsp1, RDF.type, JS.StringSchema))
            graph.add((bnitemsp1, JS.propertyName, Literal("timestamp")))
            bnitemsp2 = BNode()
            graph.add((bnitems, JS.properties, bnitemsp2))
            graph.add((bnitemsp2, RDF.type, JS.NumberSchema))
            graph.add((bnitemsp2, JS.propertyName, Literal("value")))
            for _,_,co in graph.triples((ga, COSWOT.sharesFormsWith, None)):
                d = URIRef(co[:co.rindex("#")])
                co_history = URIRef(co + "-history")
                graph.add((co_history, RDF.type, TD.PropertyAffordance))
                graph.add((d, TD.hasPropertyAffordance, co_history))
                graph.add((co_history, COSWOT.sharesFormsWith, ga_history))
                graph.add((ga_history, COSWOT.sharesFormsWith, co_history))
            httpForm = BNode(ga_history+"http")
            graph.add((ga_history, TD.hasForm, httpForm))
            graph.add((httpForm, HTV.methodName, Literal("GET")))
            graph.add((httpForm, HCTL.forContentType, Literal("text/csv")))
            graph.add((httpForm, HCTL.hasOperationType, TD.readProperty))
            graph.add((httpForm, HCTL.hasTarget, URIRef(f"https://ci.mines-stetienne.fr/mqtt/{topic}/log.csv")))


knxproj = "tempresources/2023_04_06_Espace_Fauriel_v20"
parse_knxproj(knxproj, graph)

csvfile = "tempresources/source-devices.csv"
parse_source_devices(csvfile, graph)

import os
os.makedirs("temp", exist_ok=True)
graph.serialize("temp/output.ttl", format="ttl", base=base)
