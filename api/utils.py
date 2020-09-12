# Import Neo4j driver
from neo4j import GraphDatabase
import json
import os


# Functions
#   Graph
def getGraph(word):
    # Create the driver
    db_url = os.environ.get("GRAPHENEDB_BOLT_URL")
    db_user = os.environ.get("GRAPHENEDB_BOLT_USER")
    db_pass = os.environ.get("GRAPHENEDB_BOLT_PASSWORD")
    driver = GraphDatabase.driver(db_url, auth=(db_user, db_pass), encrypted=True)

    # Create the session
    session = driver.session()
    result = session.run("MATCH (n)-[r:ASOCIA_CON]-(p:Estimulo{name:$Estimulo}) RETURN n, r, p", Estimulo=word)
    JSON = getGraphInformation(session, result)
    session.close()
    driver.close()

    return json.dumps(JSON, ensure_ascii=False, indent=4)


def getGraphInformation(session, result):
    # {
    #   name: name of the node,
    #   status: PalabrasAsociadas/PalabraEstimulo,
    #   direction: In/Out,
    #   other_nodes: {node_1, node_2}
    # }
    # .
    # .
    # .
    Argus = []
    for records in result:
        flag = False
        name = records["n"]._properties["name"]

        if (list(records["n"]._labels)[0] == "PalabrasAsociadas"):
            status = "asociada"
        else:
            status = "estimulo"

        if records["r"].nodes[0]._properties["name"] != records["p"]._properties["name"]:
            direction = "in"
        else:
            direction = "out"
        
        for result in Argus:
            if result["name"] == records["n"]._properties["name"]:
                result["direction"] = "in-out"
                flag = True
                break

        if flag: 
            continue
        
        nodes = []
        if status == "estimulo":
            other_nodes = session.run("MATCH (n)-[r:ASOCIA_CON]-(p:Estimulo{name:$Estimulo}) RETURN n, r, p LIMIT 2", Estimulo=name)
            node1, node2 = other_nodes.values()
            nodes = [node1[0]._properties["name"], node2[0]._properties["name"]]

        temporalJSON = {"name": name, "status": status, "direction": direction, "nodes": nodes}
        Argus.append(temporalJSON)

    return Argus


#   Table
def getTable(word):
    # Create the driver
    db_url = os.environ.get("GRAPHENEDB_BOLT_URL")
    db_user = os.environ.get("GRAPHENEDB_BOLT_USER")
    db_pass = os.environ.get("GRAPHENEDB_BOLT_PASSWORD")
    driver = GraphDatabase.driver(db_url, auth=(db_user, db_pass), encrypted=True)

    # Create the session
    session = driver.session()
    result = session.run("MATCH (n)-[r:ASOCIA_CON]-(p:Estimulo{name:$Estimulo}) RETURN n, r, p", Estimulo = word)

    # table:
    # [ 
    #   {
    #       "name": word,
    #       "direction": in/out,
    #       "frecuency": float,
    #       "time": float,
    #       "association": float      
    #   }
    #   .
    #   .
    # ]

    Argus = []
    for records in result:
        if(records["r"].nodes[0]._properties["name"] != "abeja"):
            name = records["r"].nodes[0]._properties["name"]
        else:
            name = records["r"].nodes[1]._properties["name"]

        if records["r"].nodes[0]._properties["name"] == records["p"]._properties["name"]:
            direction = "Out"
        else:
            direction = "In"

        frecuency = records["r"]._properties["frecuency"]
        time = records["r"]._properties["time"]
        association = records["r"]._properties["association"]
        
        temporalJSON = {"name": name, "direction": direction, "frecuency": frecuency, "time": time, "association": association}
        Argus.append(temporalJSON)

    session.close()
    driver.close()

    return json.dumps(Argus, ensure_ascii=False, indent=4)


#   Search
def getStimulus(word):
    # Create the driver
    db_url = os.environ.get("GRAPHENEDB_BOLT_URL")
    db_user = os.environ.get("GRAPHENEDB_BOLT_USER")
    db_pass = os.environ.get("GRAPHENEDB_BOLT_PASSWORD")
    driver = GraphDatabase.driver(db_url, auth=(db_user, db_pass), encrypted=True)

    # Create the session
    session = driver.session()
    # 0 - 233
    result = session.run("MATCH (n:Estimulo) WHERE n.name =~$letters RETURN n LIMIT 6", letters=(word+'.*'))
    
    Argus = []
    for records in result:
        name = records[0]._properties['name']
        temporalJSON = {"name": name}
        Argus.append(temporalJSON)

    session.close()
    driver.close()

    return json.dumps(Argus, ensure_ascii=False, indent=4)


def validation(data):
    if data != "[]":
        return data
    else:
        return "<h1>Palabra invalida</h1>"
