import re
from py2neo import Node, Relationship, Graph
import os
import json
import sqlite3
import util
import json


config = json.loads(open(util.get_rel_path('conf'), 'r').read())
DB_PATH = util.get_rel_path(config['db_path'])
DB_NAME = config['db_name']
JSON_PATH = util.get_rel_path(config['json_path'])
URL = config['url']
PASSWORD = config['password']
NAME = config['name']

conn = sqlite3.connect(DB_PATH + DB_NAME)
my_graph = Graph(URL, password=PASSWORD, name=NAME)
cur = conn.cursor()
# cur.execute('DROP TABLE graphs')
cur.execute('CREATE TABLE graphs (name TEXT, year NUMBER, month NUMBER)')
print('Table graphs created successfully.')

file_names = os.listdir(JSON_PATH)
for file_name in file_names:
    pattern = re.compile(r'(202[0123])-(\d+)')
    t = pattern.search(file_name).group()
    year, month = t.split('-', 2)
    end_index = file_name.find(t)
    name = file_name[0: end_index - 1]
    insert_sql = f"INSERT INTO graphs values ('{name}', {year}, {month})"
    cur.execute(insert_sql)
    with open(JSON_PATH + file_name, 'r') as f:
        print('processing ' + file_name)
        js_data = json.loads(f.read())
        nodes = js_data['nodes']
        links = js_data['links']
        graph_nodes = dict()
        for node in nodes:
            kind = node['c']
            graph_node = Node(kind, id=node['id'], n=node['n'], v=node['v'], year=year, month=month, repository=name)
            my_graph.create(graph_node)
            graph_nodes[node['id']] = graph_node
        for link in links:
            s = graph_nodes[link['s']]
            t = graph_nodes[link['t']]
            rel = Relationship(s, t, w=link['w'])
            my_graph.create(rel)
