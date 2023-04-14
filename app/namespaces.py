from rdflib import URIRef, Graph, SKOS, SSN, SOSA
from rdflib.namespace import Namespace, DefinedNamespace, NamespaceManager


class CDT(DefinedNamespace):
    _fail = True
    ucum: URIRef
    _NS = Namespace("https://w3id.org/cdt/")

class TD(DefinedNamespace):
    _fail = True

    Thing: URIRef
    ActionAffordance: URIRef
    EventAffordance: URIRef
    InteractionAffordance: URIRef
    OperationType: URIRef
    PropertyAffordance: URIRef
    
    definesSecurityScheme: URIRef
    hasActionAffordance: URIRef
    hasCancellationSchema: URIRef
    hasConfigurationInstance: URIRef
    hasEventAffordance: URIRef
    hasPropertyAffordance: URIRef
    hasForm: URIRef
    hasInputSchema: URIRef
    hasInteractionAffordance: URIRef
    hasLink: URIRef
    hasNotificationResponseSchema: URIRef
    hasNotificationSchema: URIRef
    hasOutputSchema: URIRef
    hasPropertyAffordance: URIRef
    hasSecurityConfiguration: URIRef
    hasSubscriptionSchema: URIRef
    hasUriTemplateSchema: URIRef
    
    description: URIRef
    descriptionInLanguage: URIRef
    isIdempotent: URIRef
    isObservable: URIRef
    isSafe: URIRef
    isSynchronous: URIRef
    name: URIRef
    title: URIRef
    titleInLanguage: URIRef
        
    cancelAction: URIRef
    invokeAction: URIRef
    observeAllProperties: URIRef
    observeProperty: URIRef
    queryAction: URIRef
    queryAllActions: URIRef
    readAllProperties: URIRef
    readMultipleProperties: URIRef
    readProperty: URIRef
    subscribeAllEvents: URIRef
    subscribeEvent: URIRef
    unobserveAllProperties: URIRef
    unobserveProperty: URIRef
    unsubscribeAllEvents: URIRef
    unsubscribeEvent: URIRef
    writeAllProperties: URIRef
    writeMultipleProperties: URIRef
    writeProperty: URIRef
 
    _NS = Namespace("https://www.w3.org/2019/wot/td#")


class HCTL(DefinedNamespace):
    _fail = True

    AdditionalExpectedResponse: URIRef
    ExpectedResponse: URIRef
    Form: URIRef
    Link: URIRef

    additionalReturns: URIRef
    hasAdditionalOutputSchema: URIRef
    hasOperationType: URIRef
    returns: URIRef

    forContentCoding: URIRef
    forContentType: URIRef
    forSubProtocol: URIRef
    hasAnchor: URIRef
    hasHreflang: URIRef
    hasRelationType: URIRef
    hasSizes: URIRef
    hasTarget: URIRef
    hintsAtMediaType: URIRef
    isSuccess: URIRef
 
    _NS = Namespace("https://www.w3.org/2019/wot/hypermedia#")

class MQV(DefinedNamespace):
    _fail = True

    controlPacket: URIRef
    retain: URIRef
    topic: URIRef
    qos: URIRef
    filter: URIRef
 
    _NS = Namespace("https://www.w3.org/2019/wot/mqtt#")
    
class HTV(DefinedNamespace):
    _fail = True

    methodName: URIRef
 
    _NS = Namespace("http://www.w3.org/2011/http#")


class COSWOT(DefinedNamespace):
    _fail = False

    KNXArea: URIRef
    KNXLine: URIRef
    Device: URIRef

    hasKNXLine: URIRef
    hasKNXDevice: URIRef
    hasStableValue: URIRef
    hasAddress: URIRef

    _NS = Namespace("https://w3id.org/coswot/")



class SCHEMA(DefinedNamespace):
    _fail = False

    model: URIRef

    _NS = Namespace("https://schema.org/")

class JS(DefinedNamespace):
    _fail = False
    _NS = Namespace("https://www.w3.org/2019/wot/json-schema#")


namespaceManager = NamespaceManager(Graph())
namespaceManager.bind("td", TD._NS)
namespaceManager.bind("coswot", COSWOT._NS)
namespaceManager.bind("schema", SCHEMA._NS)
namespaceManager.bind("hctl", HCTL._NS)
namespaceManager.bind("mqv", MQV._NS)
namespaceManager.bind("htv", HTV._NS)
namespaceManager.bind("cdt", CDT._NS)
namespaceManager.bind("skos", SKOS._NS)
namespaceManager.bind("ssn", SSN._NS)
namespaceManager.bind("sosa", SOSA._NS)
namespaceManager.bind("js", JS._NS)
