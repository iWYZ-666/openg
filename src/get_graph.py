from py2neo import Graph
import sqlite3
import re

# def get_str(args):
#     res = ''
#     for k, v in args.items():
#         if not v:
#             continue
#         if res != '':
#             res += '|'
#         res += str(k)
#     return res


def get_reverse_str(kind):
    if kind == 'i':
        return 'p|u'
    if kind == 'u':
        return 'i|p'
    if kind == 'p':
        return 'u|i'
    else:
        raise AttributeError('wrong kind.')


def process_node(nd, nid, ids, c_pattern, nodes):
    c = c_pattern.search(str(nd.labels)).group()
    node = dict(nd)
    node['id'] = nid
    node['c'] = c
    ids.add(nid)
    nodes.append(node)


def dataframe2json(df):
    ids = set()
    nodes = []
    links = []
    # real_pattern = re.compile(r'\(_(\d+)')
    # kind_pattern = re.compile(r'\(_\d+:([iurp])')
    # id_pattern = re.compile(r'id:([^,]),')
    # n_pattern = re.compile(r'n:([^,]),')
    # repo_pattern = re.compile(r' repository:([^,]),')
    # v_pattern = re.compile(r'v:([^,]),')
    # rid_pattern = re.compile(r'\(_(\d+)\)')
    # w_pattern = re.compile(r'w:([^}])}')
    # year_pattern = re.compile(r'year([^,]),')
    # month_pattern = re.compile(r'month:([^,]),')
    c_pattern = re.compile(r'([ripu])')
    for _, data in df.iterrows():
        id1 = int(data[0]['id'])
        id2 = int(data[1]['id'])
        if id1 not in ids:
            process_node(data[0], id1, ids, c_pattern, nodes)
        if id2 not in ids:
            process_node(data[1], id2, ids, c_pattern, nodes)
        sid = int(data[2].start_node['id'])
        tid = int(data[2].end_node['id'])
        w = float(data[2]['w'])
        links.append({'s': sid, 't': tid, 'w': w})
    return {'nodes': nodes, 'links': links}


def get_graph(name, year, month):
    cypher = "MATCH (a)-[l]-(b) WHERE a.repository='{}' AND a.year='{}' AND a.month='{}' RETURN a,b,l".format(
        name, year, month)
    graph = Graph('http://localhost:7474/', password='12345678', name='neo4j')
    result = graph.run(cypher).to_data_frame()
    result = dataframe2json(result)
    return result


def get_min_graph(re_name, year, month, gid, kind):
    reverse_kinds = get_reverse_str(kind)
    cypher = "MATCH (a:{})-[l]-(b:{}) WHERE a.id='{}' AND a.repository='{}' AND a.year='{}' AND a.month='{}' RETURN a,b,l".format(
        kind, reverse_kinds, gid, re_name, year, month)
    graph = Graph('http://localhost:7474/', password='12345678', name='neo4j')
    result = graph.run(cypher).to_data_frame()
    result = dataframe2json(result)
    return result


def get_repository_names():
    conn = sqlite3.connect('data/graph.db')
    cur = conn.cursor()
    cur.execute('SELECT DISTINCT name FROM graphs ORDER BY name')
    names_sql = cur.fetchall()
    names = []
    for name in names_sql:
        names.append(name[0])
    return names


def get_years(repository_name):
    conn = sqlite3.connect('data/graph.db')
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT year FROM graphs WHERE name = '{}' ORDER BY year".format(repository_name))
    years_sql = cur.fetchall()
    years = []
    for year in years_sql:
        years.append(year[0])
    return years


def get_months(repository_name, year):
    conn = sqlite3.connect('data/graph.db')
    cur = conn.cursor()
    cur.execute(
        "SELECT DISTINCT month FROM graphs WHERE name='{}' AND year={} ORDER BY month".format(repository_name,
                                                                                              year))
    months_sql = cur.fetchall()
    months = []
    for month in months_sql:
        months.append(month[0])
    return months
