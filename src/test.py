import os
import json

# 读取‘/home/liuyushi/openg/data/json’所有的文件名
JSON_PATH = '/home/liuyushi/openg/data/json/'
NAME = 'will-ww'
ID = '37722'
file_names = os.listdir(JSON_PATH)
node_dict = dict()
link_list = []
repos = []

def getNode(id, nodes: list):
    for node in nodes:
        if node["id"] == id:
            return node
    return None

def getRepo(nodes: list):
    for node in nodes:
        if node["c"] == "r":
            return node
    return None

for file_name in file_names:
    date = file_name.split('.')[1]
    repo = file_name.split('.')[0]
    # 判断date是否大于等于“2023-01”并且小于等于"2023-09",date格式为“2020-01”
    if date >= "2023-1" and date <= "2023-9":
        # 读取JSON_PATH + file_name文件
        with open(JSON_PATH + file_name, "r") as f:
            print("processing " + file_name)
            js_data = json.loads(f.read())
            nodes = js_data["nodes"]
            links = js_data["links"]
            # for node in nodes:
            #     if node["id"] == ID:
            #         node["date"] = date
            #         node["repo"] = repo
            #         if node_dict.get(repo) is None:
            #             node_dict[repo] = node
            #         else:
            #             tmp = node_dict[repo]
            #             tmp["v"] = tmp["v"] + node["v"]
            #             node_dict[repo] = tmp
            for link in links:
                if link["s"] == ID or link["t"] == ID:
                    # link operation
                    link["date"] = date
                    link["repo"] = repo
                    link_list.append(link)
                    # node operation
                    node = getNode(link["t"], nodes)
                    if node is None:
                        continue
                    if node_dict.get(link["t"]) is None:
                        node_dict[link["t"]] = node
                    else:
                        tmp = node_dict[link["t"]]
                        tmp["v"] = tmp["v"] + node["v"]
                        node_dict[link["t"]] = tmp
                    node = getNode(link["s"], nodes)
                    if node is None:
                        continue
                    if node_dict.get(link["s"]) is None:
                        node_dict[link["s"]] = node
                    else:
                        tmp = node_dict[link["s"]]
                        tmp["v"] = tmp["v"] + node["v"]
                        node_dict[link["s"]] = tmp
                    # create relationship between user and repo
                    if repo not in repos:
                        repos.append(repo)
                        tmp = getRepo(nodes)
                        if tmp is None:
                            continue
                        # create node
                        node_dict[tmp["id"]] = tmp
                        # create link
                        link_list.append({
                            "s": ID,
                            "t": tmp["id"],
                            "w": 0,
                            "date": date,
                            "repo": repo
                        })
                        
                    
                    
# get values of node_dict and make a list
node_list = []
for k,v in node_dict.items():
    node_list.append(v)
# dump node_dict to /home/liuyushi/openg/src
with open('/home/liuyushi/openg/src/node_list.json', 'w') as f:
    json.dump(node_list, f)
with open('/home/liuyushi/openg/src/link_list.json', 'w') as f:
    json.dump(link_list, f)