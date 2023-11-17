from py2neo import Graph
import duckdb
import re
import util
import json


config = json.loads(open(util.get_rel_path("conf"), "r").read())
DB_PATH = util.get_rel_path(config["db_path"])
DB_NAME = config["db_name"]
URL = config["url"]
PASSWORD = config["password"]
NAME = config["name"]


def get_reverse_str(kind):
    if kind == "i":
        return "p|u"
    if kind == "u":
        return "i|p"
    if kind == "p":
        return "u|i"
    else:
        raise AttributeError("wrong kind.")


def process_node(nd, nid, ids, c_pattern, nodes):
    c = c_pattern.search(str(nd.labels)).group()
    node = dict(nd)
    node["id"] = nid
    node["c"] = c
    ids.add(nid)
    nodes.append(node)


def dataframe2json(df):
    ids = set()
    nodes = []
    links = []
    c_pattern = re.compile(r"([ripu])")
    for _, data in df.iterrows():
        id1 = str(data[0]["id"])
        id2 = str(data[1]["id"])
        if id1 not in ids:
            process_node(data[0], id1, ids, c_pattern, nodes)
        if id2 not in ids:
            process_node(data[1], id2, ids, c_pattern, nodes)
        sid = str(data[2].start_node["id"])
        tid = str(data[2].end_node["id"])
        w = float(data[2]["w"])
        links.append({"s": sid, "t": tid, "w": w})
    return {"nodes": nodes, "links": links}


def get_graph(name, year, month):
    cypher = f"MATCH (a)-[l]-(b) WHERE a.repository='{name}' AND a.year='{year}' AND a.month='{month}' RETURN a,b,l"
    graph = Graph(URL, password=PASSWORD, name=NAME)
    result = graph.run(cypher).to_data_frame()
    result = dataframe2json(result)
    return result


def get_min_graph(re_name, year, month, gid, kind):
    reverse_kinds = get_reverse_str(kind)
    cypher = f"MATCH (a:{kind})-[l]-(b:{reverse_kinds}) WHERE a.id='{gid}' AND a.repository='{re_name}' AND a.year='{year}' AND a.month='{month}' RETURN a,b,l"
    graph = Graph(URL, password=PASSWORD, name=NAME)
    result = graph.run(cypher).to_data_frame()
    result = dataframe2json(result)
    return result


def get_repository_names():
    conn = duckdb.connect(DB_PATH + DB_NAME)
    conn.execute("SELECT DISTINCT name FROM graphs ORDER BY name")
    names_sql = conn.fetchall()
    names = []
    for name in names_sql:
        names.append(name[0])
    conn.close()
    return names


def get_years(repository_name):
    conn = duckdb.connect(DB_PATH + DB_NAME)
    conn.execute(
        f"SELECT DISTINCT year FROM graphs WHERE name = '{repository_name}' ORDER BY year")
    years_sql = conn.fetchall()
    years = []
    for year in years_sql:
        years.append(year[0])
    conn.close()
    return years


def get_months(repository_name, year):
    conn = duckdb.connect(DB_PATH + DB_NAME)
    conn.execute(
        f"SELECT DISTINCT month FROM graphs WHERE name='{repository_name}' AND year={year} ORDER BY month"
    )
    months_sql = conn.fetchall()
    months = []
    for month in months_sql:
        months.append(month[0])
    conn.close()
    return months


if __name__ == "__main__":
    print(get_repository_names())
