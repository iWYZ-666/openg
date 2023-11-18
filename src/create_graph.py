import re
from py2neo import Node, Relationship, Graph, Subgraph
import os
import json
import duckdb
import util
import json

# config
config = json.loads(open(util.get_rel_path("conf"), "r").read())
DB_PATH = util.get_rel_path(config["db_path"])
DB_NAME = config["db_name"]
JSON_PATH = util.get_rel_path(config["json_path"])
URL = config["url"]
PASSWORD = config["password"]
NAME = config["name"]

table_dict = {"r": "repositories", "u": "users", "i": "issues", "p": "prs"}
link_dict = {"ru": "repository_user", "ri": "repository_issue",
             "rp": "repository_pr", "ui": "user_issue", "up": "user_pr"}

# clear sqlite
if os.path.exists(DB_PATH + DB_NAME):
    os.remove(DB_PATH + DB_NAME)
# connected to sqlite
conn = duckdb.connect(DB_PATH + DB_NAME)
conn.execute(
    "CREATE TABLE graphs (name VARCHAR(30), year INTEGER, month INTEGER)")
for table_name in table_dict.values():
    conn.execute(
        f"CREATE TABLE {table_name} (id INTEGER, name VARCHAR(30), year INTEGER, month INTEGER, rank DOUBLE)")
# conn.execute(
#     "CREATE TABLE users (id INTEGER, name VARCHAR(30), year INTEGER, month INTEGER, rank DOUBLE)")
# conn.execute(
#     "CREATE TABLE repositories (id INTEGER, name VARCHAR(30), year INTEGER, month INTEGER, rank DOUBLE)")
# conn.execute(
#     "CREATE TABLE issues (id INTEGER, name VARCHAR(30), year INTEGER, month INTEGER, rank DOUBLE)")
# conn.execute("CREATE TABLE prs (id INTEGER, name VARCHAR(30), )")
# conn.execute(
#     "CREATE TABLE repository-user (fid INTEGER, sid INTEGER, year INTEGER, month INTEGER)")
# conn.execute(
#     "CREATE TABLE repository-issue (fid INTEGER, sid INTEGER, year INTEGER, month INTEGER)")
# conn.execute(
#     "CREATE TABLE repository-pr (fid INTEGER, sid INTEGER, year INTEGER, month INTEGER)")
# conn.execute(
#     "CREATE TABLE user-issue (fid INTEGER, sid INTEGER, year INTEGER, month INTEGER)")
# conn.execute(
#     "CREATE TABLE user-pr (fid INTEGER, sid INTEGER, year INTEGER, month INTEGER)")
# conn.execute(
#     "CREATE TABLE issue-pr (fid INTEGER, sid INTEGER, year INTEGER, month INTEGER)")
for link_name in link_dict.values():
    conn.execute(
        f"CREATE TABLE {link_name} (fid INTEGER, sid INTEGER, year INTEGER, month INTEGER, weight DOUBLE)")
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


def merge_kinds(first_kind: str, second_kind: str, first_id: str, second_id: str):
    flag = False
    kind = ""
    if (first_kind == "r"):
        kind = f"r{second_kind[0]}"
    elif (second_kind == "r"):
        kind = f"r{first_kind[0]}"
        flag = True
    elif (first_kind == "u"):
        kind = f"u{second_kind[0]}"
    elif (second_kind == "u"):
        kind = f"u{first_kind[0]}"
        flag = True
    elif (first_kind == "i"):
        kind = f"i{second_kind[0]}"
    else:
        kind = f"i{first_kind[0]}"
        flag = True
    if flag:
        return kind, second_id, first_id
    return kind, first_id, second_id


def execute_insert_table(id: str, name: str, year: str, month: str, rank: float, kind: str):
    table_name = table_dict[kind]
    conn.execute(
        f"INSERT INTO {table_name} VALUES ({id}, '{name}', {year}, {month}, {rank})")


def excute_insert_link(first_id: str, second_id: str, year: str, month: str, weight: str, kind: str) -> None:
    link_name = link_dict[kind]
    conn.execute(
        f"INSERT INTO {link_name} VALUES ({first_id}, {second_id}, {year}, {month}, {weight})")


file_names = os.listdir(JSON_PATH)
for file_name in file_names:
    pattern = re.compile(r"(202[0123])-(\d+)")
    t = pattern.search(file_name).group()
    year, month = t.split("-", 2)
    end_index = file_name.find(t)
    name = file_name[0: end_index - 1]
    conn.execute(f"INSERT INTO graphs VALUES ('{name}', {year}, {month})")
    id2kind = dict()
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
            id2kind[node["id"]] = kind
            node_list.append(graph_node)
            graph_nodes[node["id"]] = graph_node
            execute_insert_table(
                node["id"], node["n"], year, month, node["v"], kind)
        for link in links:
            s = graph_nodes.get(link["s"])
            t = graph_nodes.get(link["t"])
            if s and t:
                s_kind = id2kind[link["s"]]
                t_kind = id2kind[link["t"]]
                rel = Relationship(s, t, w=link["w"])
                # my_graph.create(rel)
                link_list.append(rel)
                m_kind, fid, sid = merge_kinds(
                    s_kind, t_kind, link["s"], link["t"])
                excute_insert_link(fid, sid, year, month, link["w"], m_kind)

        batch_load(node_list, link_list, my_graph)
    conn.commit()
conn.close()
