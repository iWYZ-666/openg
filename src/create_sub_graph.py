import re
from py2neo import Node, Relationship, Graph
import json
import sqlite3
import glob
import util
import json


config = json.loads(open(util.get_rel_path('conf'), 'r').read())
DB_PATH = util.get_rel_path(config['db_path'])
DB_NAME = config['db_name']
JSON_PATH = util.get_rel_path(config['json_path'])
JSON_PATH = util.get_rel_path(config['json_path'])
URL = config['url']
PASSWORD = config['password']
NAME = config['name']

conn = sqlite3.connect(DB_PATH + DB_NAME)
my_graph = Graph(URL, password=PASSWORD, name=NAME)
cur = conn.cursor()
cur.execute('CREATE TABLE graphs (name TEXT, year NUMBER, month NUMBER)')
conn.commit()
repos = ['alibaba-arthas', 'alibaba-canal', 'alibaba-druid', 'alibaba-easyexcel', 'kubevela-velaux',
         'kubevela-workflow', 'labring-laf', 'labring-sealos', 'midwayjs-midway', 'nacos-group-nacos-k8s',
         'redis-redis', 'X-lab2017-open-digger']
for repo in repos:
    for file in glob.glob("{}{}*.json".format(JSON_PATH,repo)):
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
cur.close()
conn.close()