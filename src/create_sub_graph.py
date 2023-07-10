import re
from py2neo import Node, Relationship, Graph
import json
import sqlite3
import glob

conn = sqlite3.connect('../data/graph.db')
my_graph = Graph('http://localhost:7474/', password='12345678', name='neo4j')
cur = conn.cursor()
cur.execute('CREATE TABLE graphs (name TEXT, year NUMBER, month NUMBER)')
repos = ['alibaba-arthas', 'alibaba-canal', 'alibaba-druid', 'alibaba-easyexcel', 'kubevela-velaux',
         'kubevela-workflow', 'labring-laf', 'labring-sealos', 'midwayjs-midway', 'nacos-group-nacos-k8s',
         'redis-redis', 'X-lab2017-open-digger']
for repo in repos:
    for file in glob.glob("../data/{}*.json".format(repo)):
        print(file)
        pattern = re.compile(r'(202[0123])-(\d+)')
        t = pattern.search(file).group()
        year, month = t.split('-', 2)
        end_index = file.find(t)
        insert_sql = "INSERT INTO graphs VALUES('{}',{},{})".format(repo, year, month)
        cur.execute(insert_sql)
        conn.commit()
        with open(file, 'r') as f:
            js_data = json.loads(f.read())
            nodes = js_data['nodes']
            links = js_data['links']
            graph_nodes = dict()
            for node in nodes:
                kind = node['c']
                graph_node = Node(kind, id=node['id'], n=node['n'], v=node['v'], year=year, month=month,
                                  repository=repo)
                my_graph.create(graph_node)
                graph_nodes[node['id']] = graph_node
            for link in links:
                s = graph_nodes[link['s']]
                t = graph_nodes[link['t']]
                rel = Relationship(s, t, w=link['w'])
                my_graph.create(rel)
