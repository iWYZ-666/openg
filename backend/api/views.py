from django.http.response import JsonResponse
# from pydantic import Json
from backend.function import check_method, get_post_json
from pyecharts.commons.utils import JsCode
import json
import requests
import pyecharts.options as opts
from pyecharts.charts import Graph, Timeline
import random
import os
from django.conf import settings
import time
import copy
from tqdm import tqdm
# =====================================协作网络检索部分==============================
def get_Network_Search_data_pre():
    resp = requests.get("https://oss.x-lab.info/open_digger/github/X-lab2017/open-digger/project_openrank_detail/2022-12.json")
    data = resp.json()
    return data["nodes"], data["links"]
ns_nodes, ns_edges = get_Network_Search_data_pre()
def get_Network_Search_info(name, year, month):
    # todo
    # 输入的参数可以改
    user, pr, issue = 0, 0, 0
    for node in ns_nodes:
        if node["c"] == "u":
            user += 1
        if node["c"] == "p":
            pr += 1
        if node["c"] == "i":
            issue += 1
    return user, pr, issue
def get_Network_Search_OpenRank(name, year, month):
    # todo
    # 输入的参数可以改
    OpenRank_dict = {}
    for node in ns_nodes:
        if node["n"] not in OpenRank_dict:
            OpenRank_dict[node["n"]] = node["v"]
        else:
            OpenRank_dict[node["n"]] += node["v"]
    sorted_item = sorted(OpenRank_dict.items(), key=lambda x: x[1], reverse=True)
    return [{"index": i + 1, "rank": round(sorted_item[i][1], 2), "name": sorted_item[i][0]}for i in range(len(sorted_item))]
def get_Network_Search_Graph(name, year, month):
    # todo
    # 输入的参数可以改
    fake_nodes = [
            {"id": "0x75cd2467f8dd731a5acb927bd79c4cb361210db6", "degree": 2},
            {"id":"0xc611952d81e4ecbd17c8f963123dec5d7bce1c27", "degree": 2},
            {"id":"0x4de23f3f0fb3318287378adbde030cf61714b2f3", "degree":1}
        ],
    fake_edges = [
            {"source": "0x75cd2467f8dd731a5acb927bd79c4cb361210db6", "target": "0xc611952d81e4ecbd17c8f963123dec5d7bce1c27", "value": "299928147539103754", "tx_hash": "0xa1a658f372e0637d00b78753036068d71d48da9d6a924e8f6443bc3e5bbec940", "blockNumber": "15265907"},
            {"source": "0x75cd2467f8dd731a5acb927bd79c4cb361210db6", "target": "0x4de23f3f0fb3318287378adbde030cf61714b2f3", "value": "9000000000000000", "tx_hash": "0x0dcf54ffa7d83238b8a44a9c2385a2d58a9f0d326116f293ba351076dbb38d4a", "blockNumber": "15265929"},
            {"source": "0x8bc90377daf1b4e71686d025c88b2178089cf3e8", "target": "0xc611952d81e4ecbd17c8f963123dec5d7bce1c27", "value": "2611540377663885806", "tx_hash": "0x5ff169a9301adf698f6e78bd8c715aebb7fdd5404e24ef5b926a10adbc1b8772", "blockNumber": "15265903"},
            {"source": "0x1a26db1b2baf0b23f18e19375e8fdc159feb707e", "target": "0xc611952d81e4ecbd17c8f963123dec5d7bce1c27", "value": "473558773599046477", "tx_hash": "0xc708b1f3315db9966a677782efc896364803cb457cdfc2ae76ff9141935fd532", "blockNumber": "15265905"},
            {"source": "0x43da6d2db9651b7042e31ffb2607a7cfa4d5d03b", "target": "0xc611952d81e4ecbd17c8f963123dec5d7bce1c27", "value": "621618643271362538", "tx_hash": "0x51927ba1b63a5adf90dc8a673b459c9e5e3e42c2ae3157ca57ae7a54232c75a0", "blockNumber": "15265905"},
            {"source": "0xe5c04c954c5494f6975f63e3f19957a380648f82", "target": "0xc611952d81e4ecbd17c8f963123dec5d7bce1c27", "value": "223324337176025309", "tx_hash": "0x0c3ecd77775785129d70adcb43c656c854f22699f3350aa17693af608d3729ee", "blockNumber": "15265907"},
            {"source": "0x795d8f8b2bf1bb23e99e165c8e4fa067d96cb00a", "target": "0xc611952d81e4ecbd17c8f963123dec5d7bce1c27", "value": "216300000000000000", "tx_hash": "0xf59060ff06f14fd261a81272b562afe7c4a9a5642ead937962858a8f54a601b9", "blockNumber": "15265907"},
            {"source": "0xbdf4cf8269c3883dd88975e1978a6aa9d3877f2e", "target": "0xc611952d81e4ecbd17c8f963123dec5d7bce1c27", "value": "288173851825282417", "tx_hash": "0x851c13f6fd11fe61bc40e6f071d1bd1fb2b667adbed715534c3a631c48c5eb49", "blockNumber": "15265907"},
            {"source": "0x1e29e2cefd3395d892678add3eb791ed74114f3b", "target": "0xc611952d81e4ecbd17c8f963123dec5d7bce1c27", "value": "284693896987212129", "tx_hash": "0x1ddbf38bf57786d3e1079cc53a81168f0b7ac958b838bdfeb6a77dfb1cc134af", "blockNumber": "15265907"},
            {"source": "0x47537db3dfec13e9f20fb4f4cd0cf26e2cc37fdd", "target": "0xc611952d81e4ecbd17c8f963123dec5d7bce1c27", "value": "265102276730551319", "tx_hash": "0x24dca1ae019a880520049e5ac75d6a49c009cb3dfe59de0b6261859070ec0ae3", "blockNumber": "15265907"},
            {"source": "0x4842336fdaf0405e12c7e968dc1998856672a4d7", "target": "0xc611952d81e4ecbd17c8f963123dec5d7bce1c27", "value": "373844808070480320", "tx_hash": "0xec5da3e3ec57dc29b534888f9874b1733f0d425518180bce2ba8e2511ac4119c", "blockNumber": "15266086"},
            {"source": "0x6e8b6af9d8b402d89d1f5d8c1cf535850dc28b98", "target": "0xc611952d81e4ecbd17c8f963123dec5d7bce1c27", "value": "116709184816773670", "tx_hash": "0x8992fd93bc4dd5fb7a811718313802cc4b6043a9aad6ef847c35ebb47326273a", "blockNumber": "15266104"},
            {"source": "0xa789d472cfef01e09674e4a6c03b35c72e0bfdb0", "target": "0xc611952d81e4ecbd17c8f963123dec5d7bce1c27", "value": "1847142590831247533", "tx_hash": "0x18e0e10013a4d14535f465e54f051c34607f4c654b2c59a6ac58e5588ee07363", "blockNumber": "15266490"},
        ]
    nodes = fake_nodes
    edges = fake_edges
    return {"nodes": nodes, "edges": edges}
@check_method('POST')
def Network_Search_view(request):
    post = get_post_json(request=request) # 获取post请求内容
    # post内容
        # name: 仓库名, year: 年份, month: month
    name, year, month = post['name'], post['year'], post['month']
# 返回内容
    # 1、用户数、pr数、issue数 + 查询内容name、year、month
    userNumber, pr, issue = get_Network_Search_info(name, year, month)

    # 2、每个节点按OpenRank的排序
        # {"name": "节点名", "rank": "openRank值", "index": "排序"}
    openRank = get_Network_Search_OpenRank(name, year, month)

    # 3、Graph图内容
        # 分为两部分: nodes, edges
            # nodes: [{"id": "节点id", 后续属性待定}]
            # edges: [{"source": "节点id", "target": "节点id", 后续属性待定}]
    graphOption = get_Network_Search_Graph(name, year, month)
    return JsonResponse({
        'message': 'ok',
        "info": {
            "userNumber": userNumber,
            "pr": pr,
            "issue": issue,
            "name": name,
            "year": year,
            "month": month
        },
        "openRank": openRank,
        "option": graphOption
    })
#==========================================================================


# =====================================协作网络分析部分==============================
def get_Network_Analyze_line_data_pre():
    index = ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"]
    issue_data = []
    request_data = []
    user_data = []
    total_nodes = []
    for i in tqdm(range(1, 13)):
        format_index = str(i) if i >= 10 else "0" + str(i)
        resp = requests.get("https://oss.x-lab.info/open_digger/github/X-lab2017/open-digger/project_openrank_detail/2022-{}.json".format(format_index))
        # print(resp)
        data = resp.json()
        request, issue, user = 0, 0, 0
        total_nodes.append(data["nodes"])
        for node in data["nodes"]:
            # pr request
            if node["c"] == "p":
                request += 1
            elif node["c"] == "u":
                user += 1
            elif node["c"] == "i":
                issue += 1
        issue_data.append([index[i - 1], issue])
        request_data.append([index[i - 1], request])
        user_data.append([index[i - 1], user])
    return total_nodes, request_data, issue_data, user_data
na_nodes, na_request_data, na_issue_data, na_user_data = get_Network_Analyze_line_data_pre()
def get_Network_Analyze_line_data(name, year):
    # todo
    # 输入的参数可以改
    # 这里的格式不要换，是pyecharts转化的json的格式
    issue_data, request_data, user_data = na_issue_data, na_request_data, na_user_data
    return {
        "issue": issue_data,
        "request": request_data,
        "user": user_data
    }
def get_Network_Analyze_pie_data(name, year):
    # todo
    # 输入的参数可以改
    # 这里的格式不要换，是pyechars转化的json的格式
    fake_data = [
        {
            "name": "Core Developers",
            "value": 100
        },
        {
            "name": "Temporary Developers",
            "value": 20
        },
        {
            "name": "Issue Participants",
            "value": 50
        }
    ]
    data = fake_data
    return data

def get_Network_Analyze_OpenRank(name, year):
    # todo
    # 输入的参数可以改
    OpenRank_dict = {}
    for nodes in na_nodes:
        for node in nodes:
            if node["n"] not in OpenRank_dict:
                OpenRank_dict[node["n"]] = node["v"]
            else:
                OpenRank_dict[node["n"]] += node["v"]
    sorted_item = sorted(OpenRank_dict.items(), key=lambda x: x[1], reverse=True)
    return [{"index": i + 1, "rank": round(sorted_item[i][1], 2), "name": sorted_item[i][0]}for i in range(len(sorted_item))]
    # data = fake_data
    # return data
def get_Network_Analyze_info(line_data):
    # todo
    # 输入的参数可以改
    total_r, total_i, total_u = 0, 0, 0
    for item in line_data["request"]:
        total_r += item[1]
    for item in line_data["issue"]:
        total_i += item[1]
    for item in line_data["user"]:
        total_i += item[1]
    return total_r, total_i, total_u
@check_method('POST')
def Network_Analyze_view(request):
    post = get_post_json(request)
    # post内容
        # name: 仓库名, year: 年份
    name ,year = post["name"], post["year"]
    print(post)
# 返回内容
    # 1、按照p2中的内容，首先折线图
        # issue、Pull Request、Users在各个月份的数据
    line_data = get_Network_Analyze_line_data(name, year)
    # 2、饼图 这个前端注释掉了，后端先留着
        # Core Developers、 Temporary Developers、Issue Participants
    pie_data = get_Network_Analyze_pie_data(name, year)
    # 3、OpenRank
    openRank = get_Network_Analyze_OpenRank(name, year)
    # 4、 request、pr、issue总数 + 查询内容
    request, user, issue = get_Network_Analyze_info(line_data)
    return JsonResponse({
        "info": {
            "request": request,
            "user": user,
            "issue": issue,
            "name": name,
            "year": year
        },
        "message": 'ok',
        "line": line_data,
        "pie": pie_data,
        'openRank': openRank
    })
#==========================================================================



# =====================================用户行为分析部分==============================
# 如果需要可以对year, month定义结构体
class Struct4YearAndMonth:
    def __init__(self, year, month):
        self.year = year
        self.month = month
    def toString(self):
        return "{}-{}".format(self.year, self.month)
    # 这里可以转化为需要的时间format格式
    def toYourFormat(self):
        return "{}-{}".format(self.year, self.month)
def get_User_Analyze_info(line_data): 
    total_r, total_p, total_i = 0, 0, 0
    for item in line_data["project"]:
        total_r += item[1]
    for item in line_data["issue"]:
        total_i += item[1]
    for item in line_data["pr"]:
        total_p += item[1]
    return total_r, total_p, total_i

def get_month_range(startYear, endYear, startMonth, endMonth):
    print(startYear, endYear)
    years = list(range(int(startYear), int(endYear) + 1))
    # print(years)
    result = []
    for year in years:
        # 起始年和结束年相同，只要判断月份,这里从简不考虑起始小于终止
        if len(years) == 1:
            for month in range(int(startMonth), int(endMonth) + 1):
                result.append(Struct4YearAndMonth(year, month).toString())
        else:
            if year == int(startYear):
                for month in range(int(startMonth), 13):
                    result.append(Struct4YearAndMonth(year, month).toString())
            elif year == int(endYear):
                for month in range(1, int(endMonth) + 1):
                    result.append(Struct4YearAndMonth(year, month).toString())
            else:
                for month in range(1, 13):
                    result.append(Struct4YearAndMonth(year, month).toString())
    return result
def get_User_Analyze_line_data(name, startYear, endYear, startMonth, endMonth):
    # 这里由于有年和月，所以需要写成年-月的形式递增
    # 真实使用的时候把startYear, endYear, startMonth, endMonth传入
    x_label = get_month_range(startYear, endYear, startMonth, endMonth)
    project_dict = {}
    pr_dict = {}
    issue_dict = {}
    r_id = ua_nodes[0]["id"]
    node_dict = {}
    for node in ua_nodes:
        node_dict[node["id"]] = node["c"] 
    for x in x_label:
        project_dict[x] = 0
        pr_dict[x] = 0
        issue_dict[x] = 0
    for edge in ua_edges:
        date = edge["date"]
        c = 'i'
        if edge["s"] == r_id:
            c = node_dict[edge["t"]]
        if edge["t"] == r_id:
            c = node_dict[edge["s"]]
        if c == "r":
            project_dict[date] += 1
        if c == "i":
            issue_dict[date] += 1
        if c == 'p':
            pr_dict[date] += 1

    # fake_project_data = [[x, random.randint(1, 100)]for x in fake_x_label]
    # fake_pr_data = [[x, random.randint(1, 100)]for x in fake_x_label]
    # fake_issue_data = [[x, random.randint(1, 100)]for x in fake_x_label]
    project_data = [[x, project_dict[x]] for x in x_label]
    pr_data = [[x, pr_dict[x]] for x in x_label]
    issue_data = [[x, issue_dict[x]] for x in x_label]
    # x = fake_x_label
    return {
        "project": project_data,
        "pr": pr_data,
        "issue": issue_data,
        "x": x_label
    }
def get_User_Analyze_pie_data(name, startYear, endYear, startMonth, endMonth):
    # 这里先给下饼图里的各个数据是啥
    with open("./api/data/pie.json") as f:
        data = json.load(f)
        f.close()
    labels = []
    result = []
    for item in data:
        labels.append(item["repo"])
        result.append({"name": item["repo"], "value": round(item["v"],2)})
    # return result
    # labels = ["类别1", "类别2", "类别3"]
    # fake_data = [{"name": label, "value": random.randint(1, 100)} for label in labels]
    # data = fake_data
    print(result)
    return {
        "label": labels,
        "data": result
    }
def get_User_Analyze_Graph_pre():
    with open("./api/data/link_list_p3.json") as f:
        edges = json.load(f)
        f.close()
    for edge in edges:
        edge["source"] = edge["s"]
        edge["target"] = edge["t"]
    with open("./api/data/node_list_p3.json") as f:
        nodes= json.load(f)
    return nodes, edges
ua_nodes, ua_edges = get_User_Analyze_Graph_pre()
def get_User_Analyze_Graph(name, startYear, endYear, startMonth, endMonth):
    # todo
    # 输入的参数可以改
    nodes = ua_nodes
    edges = ua_edges
    return {"nodes": nodes, "edges": edges}
@check_method('POST')
def User_Analyze_view(request):
    post = get_post_json(request)
    # post内容
        # name: 用户名, "startYear": 起始年, "endYear": 结束年, "startMonth": 起始月, "endMonth": 结束月
    name, startYear, endYear, startMonth, endMonth = post["name"], post["startYear"], post["endYear"], post["startMonth"], post["endMonth"]
# 返回内容

    # 1、 折线图数据，这里先写的上述数据的每个月数据，也就是每个月参与项目数、pr数、issue数
    line_data = get_User_Analyze_line_data(name, startYear, endYear, startMonth, endMonth)
    # print(line_data)
    # 2、参与项目数、pr数、提交issue数 + 查询内容name, startYear, endYear, startMonth, endMonth
    project, pr, issue = get_User_Analyze_info(line_data)
    
    # 3、饼图数据，OpenRank的数据我不清楚是啥，所以下面需要给出一下
    pie_data = get_User_Analyze_pie_data(name, startYear, endYear, startMonth, endMonth)
    
    # 4、Graph图内容
        # 分为两部分: nodes, edges
            # nodes: [{"id": "节点id", 后续属性待定}]
            # edges: [{"source": "节点id", "target": "节点id", 后续属性待定}]
    option = get_User_Analyze_Graph(name, startYear, endYear, startMonth, endMonth)
    return JsonResponse({
        "info": {
            "name": name,
            "time": {
                "start":{
                    "year": startYear,
                    "month": startMonth
                },
                "end": {
                    "year": endYear,
                    "month": endMonth
                }
            },
            "project": project,
            "pr": pr,
            "issue": issue 
        },
        "line": line_data,
        "pie": pie_data,
        "option": option
    })