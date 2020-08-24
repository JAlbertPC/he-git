# Import Neo4j driver
from neo4j import GraphDatabase
import json
import os


# things to use: get, _id, _labels (list), _propierties
# {
#   name: name of the node,
#   status: PalabrasAsociadas/PalabraEstimulo,
#   direction: In/Out,
#   other_nodes: {node_1, node_2}
# }

# Functions
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
    Argus = []
    for records in result:
        name = records["n"]._properties["name"]
        status = list(records["n"]._labels)[0]

        if records["r"].nodes[0]._properties["name"] == records["p"]._properties["name"]:
            direction = "Out"
        else:
            direction = "In"

        nodes = []
        if (status == "PalabraEstimulo") or (status == "Estimulo"):
            other_nodes = session.run("MATCH (n)-[r:ASOCIA_CON]-(p:Estimulo{name:$Estimulo}) RETURN n, r, p LIMIT 2",
                                      Estimulo=name)
            node1, node2 = other_nodes.values()
            nodes = [node1[0]._properties["name"], node2[0]._properties["name"]]

        temporalJSON = {"name": name, "status": status, "direction": direction, "nodes": nodes}
        Argus.append(temporalJSON)

    return Argus
