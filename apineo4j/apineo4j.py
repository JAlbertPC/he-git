# Import Neo4j driver
from neo4j import GraphDatabase
import json
import os


# Functions
#   Graph
def getData(word):
    # Create the driver
    db_url = os.environ.get("GRAPHENEDB_BOLT_URL")
    db_user = os.environ.get("GRAPHENEDB_BOLT_USER")
    db_pass = os.environ.get("GRAPHENEDB_BOLT_PASSWORD")
    driver = GraphDatabase.driver(db_url, auth=(db_user, db_pass), encrypted=True)

    # Create the session
    session = driver.session()
    result = session.run("MATCH (n)-[r:ASOCIA_CON]-(p:Estimulo{name:$Estimulo}) RETURN n, r, p", Estimulo=word)
    exportJSON = generateJSON(session, result)
    session.close()
    driver.close()

    return json.dumps(exportJSON, ensure_ascii=False, indent=4)


def generateJSON(session, result):
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
        status = list(records["n"]._labels)[0]

        if records["r"].nodes[0]._properties["name"] != records["p"]._properties["name"]:
            direction = "In"
        else:
            direction = "Out"
        
        for result in Argus:
            if result["name"] == records["n"]._properties["name"]:
                result["direction"] = ["In", "Out"]
                flag = True
                break

        if flag: 
            continue
        
        nodes = []
        if (status == "PalabraEstimulo") or (status == "Estimulo"):
            other_nodes = session.run("MATCH (n)-[r:ASOCIA_CON]-(p:Estimulo{name:$Estimulo}) RETURN n, r, p LIMIT 2", Estimulo=name)
            node1, node2 = other_nodes.values()
            nodes = [node1[0]._properties["name"], node2[0]._properties["name"]]

        temporalJSON = {"name": name, "status": status, "direction": direction, "nodes": nodes}
        Argus.append(temporalJSON)

    return Argus


#   Table
def generateTableJSON(word):
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
def allStimulus(word):
    # Create the driver
    db_url = os.environ.get("GRAPHENEDB_BOLT_URL")
    db_user = os.environ.get("GRAPHENEDB_BOLT_USER")
    db_pass = os.environ.get("GRAPHENEDB_BOLT_PASSWORD")
    driver = GraphDatabase.driver(db_url, auth=(db_user, db_pass), encrypted=True)

    # Create the session
    session = driver.session()
    #0 - 233
    result = session.run("MATCH (n:Estimulo) WHERE n.name =~$letters RETURN n LIMIT 6", letters=(word+'.*'))
    
    Argus = []
    for records in result:
        name = records[0]._properties['name']
        temporalJSON = {"name": name}
        Argus.append(temporalJSON)

    session.close()
    driver.close()

    return json.dumps(Argus, ensure_ascii=False, indent=4)
