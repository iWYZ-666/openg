# import re
# from py2neo import Node, Relationship, Graph
# import os
# import json
# import sqlite3
#
# conn = sqlite3.connect('../data/graph.db')
# my_graph = Graph('http://localhost:7474/', password='12345678', name='neo4j')
# cur = conn.cursor()
# cur.execute('CREATE TABLE graphs (name TEXT, year NUMBER, month NUMBER)')
# dir_path = '../data/'
# file_names = os.listdir(dir_path)
# for file_name in file_names:
#     if not file_name.endswith('json'):
#         continue
#     pattern = re.compile(r'(202[0123])-(\d+)')
#     t = pattern.search(file_name).group()
#     year, month = t.split('-', 2)
#     end_index = file_name.find(t)
#     name = file_name[0: end_index - 1]
#     insert_sql = "INSERT INTO graphs values ('{}', {}, {})".format(name, year, month)
#     with open(dir_path + file_name, 'r') as f:
#         js_data = json.loads(f.read())
#         nodes = js_data['nodes']
#         links = js_data['links']
#         graph_nodes = dict()
#         for node in nodes:
#             kind = node['c']
#             graph_node = Node(kind, id=node['id'], n=node['n'], v=node['v'], year=year, month=month, repository=name)
#             my_graph.create(graph_node)
#             graph_nodes[node['id']] = graph_node
#         for link in links:
#             s = graph_nodes[link['s']]
#             t = graph_nodes[link['t']]
#             rel = Relationship(s, t, w=link['w'])
#             my_graph.create(rel)
