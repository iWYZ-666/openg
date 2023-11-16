import re
from py2neo import Node, Relationship, Graph, Subgraph
import os
import json
import sqlite3
import util
import json
import time

# config
config = json.loads(open(util.get_rel_path("conf"), "r").read())
DB_PATH = util.get_rel_path(config["db_path"])
DB_NAME = config["db_name"]
JSON_PATH = util.get_rel_path(config["json_path"])
URL = config["url"]
PASSWORD = config["password"]
NAME = config["name"]

# clear sqlite
if os.path.exists(DB_PATH + DB_NAME):
    os.remove(DB_PATH + DB_NAME)
# connected to sqlite
conn = sqlite3.connect(DB_PATH + DB_NAME)
cur = conn.cursor()
cur.execute("CREATE TABLE graphs (name TEXT, year NUMBER, month NUMBER)")
conn.commit()

# connected to neo4j
my_graph = Graph(URL, password=PASSWORD, name=NAME)
# clear neo4j
my_graph.delete_all()

# load a subgraph into the graph
def batch_load(node_list: [], link_list: [], graph: Graph):
    subgraph = Subgraph(node_list, link_list)
    tx_ = graph.begin()
    tx_.create(subgraph)
    graph.commit(tx_)


file_names = os.listdir(JSON_PATH)
for file_name in file_names:
    pattern = re.compile(r"(202[0123])-(\d+)")
    t = pattern.search(file_name).group()
    year, month = t.split("-", 2)
    end_index = file_name.find(t)
    name = file_name[0 : end_index - 1]
    insert_sql = f"INSERT INTO graphs values ('{name}', {year}, {month})"
    cur.execute(insert_sql)
    node_list = []
    link_list = []
    with open(JSON_PATH + file_name, "r") as f:
        print("processing " + file_name)
        js_data = json.loads(f.read())
        nodes = js_data["nodes"]
        links = js_data["links"]
        graph_nodes = dict()
        for node in nodes:
            kind = node["c"]
            graph_node = Node(
                kind,
                id=node["id"],
                n=node["n"],
                v=node["v"],
                year=year,
                month=month,
                repository=name,
            )
            # my_graph.create(graph_node)
            node_list.append(graph_node)
            graph_nodes[node["id"]] = graph_node
        for link in links:
            s = graph_nodes.get(link["s"])
            t = graph_nodes.get(link["t"])
            if s and t:
                rel = Relationship(s, t, w=link["w"])
                # my_graph.create(rel)
                link_list.append(rel)
        batch_load(node_list, link_list, my_graph)
    conn.commit()
cur.close()
conn.close()
