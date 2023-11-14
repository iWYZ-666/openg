## 环境准备

首先请确保环境中安装wget，python3，输入如下命令安装第三方python库：

~~~bash
pip install -r requirements.txt
~~~

使用Docker部署Neo4j

```shell
docker run -d \
    --publish=7474:7474 --publish=7687:7687 \
    --volume=$HOME/neo4j/data:/data \
    neo4j
```

## 数据准备

输入如下命令获取数据集：

~~~bash
python3 src/download_json.py
~~~

输入如下命令建立Neo4j与sqlite数据库：

~~~bash
python3 src/create_graph.py
~~~

## 运行项目

输入如下命令运行本项目：

~~~bash
python3 main.py
~~~

在浏览器中访问localhost:5000即可访问。

## 小组成员

|  姓名  |    学号     |
| :----: | :---------: |
| 刘雨石 | 51255903113 |
|  卫涛  | 51255903105 |
| 程奂仑 | 51255903112 |
| 胡展翊 | 51255903110 |

## 思路

​	我们选择的题目是**W3：开源协作网络可视化**，在 GitHub 中，开源协作从单纯的 Git 代码协作扩大为基于 Issue、Pull Request、Discussion、Follow 等 GitHub 特性的多维协作。协作建立联系，联系构造网络，通过构造网络、分析网络并可视化网络的方式展现开源协作数据，开源世界将更好地被人们洞察。在网络构建方面，我们进一步选择了**项目内的协作网络数据**。该题目所提供的数据为项目的协作网络数据，以月为维度发布，支持阿里开源开发者贡献榜、XSOSI 项目等共计 73 个仓库的数据。此外，观察到数据主要分为以下两个类型：

- nodes 为节点：
  - id 为节点唯一标识
  - n 为节点名，包含仓库、开发者、Issue/PR number
  - c 为类型，r 是仓库，u 是开发者，i 是 Issue，p 是 PR
  - v 是当月 OpenRank 值

- links 为边
  - s 为边起点
  - t 为边终点
  - w 为边权重


​	面对以大量点、边数据构成的数据集，我们选择使用**图数据库Neo4j**对其进行存储，原因如下：

- 图数据模型：Neo4j使用图数据模型，可以轻松表示和存储复杂的关系和连接。这使得Neo4j非常适合处理具有大量关联性的数据，例如社交网络、知识图谱和推荐系统。
- 高性能：Neo4j通过使用图数据库引擎来优化查询性能。这种引擎利用了图结构的特性，可以快速导航和遍历图形数据。因此，Neo4j能够在处理大规模数据集时提供高效的查询和分析能力。
- 实时查询：Neo4j支持实时查询，这意味着您可以立即从图数据库中检索数据。这对于需要快速响应查询的应用程序非常重要，例如实时推荐和欺诈检测。

​	在完成了数据库的选型后，我们需要考虑如何将查询结果可视化，一个良好的开源协作网络可视化图应该具备但不限于以下几个特点：

- 准确：可视表达时不歪曲，不误导，不遗漏，精准如实反应数据的特征信息；
- 清晰：清晰包括两个层面，结构清晰与内容清晰；
  - 结构清晰：数据可视化呈现的是一幅作品，它是制作者分析思路的呈现，其布局决定用户的浏览顺序；
  - 内容清晰：不让用户带着疑惑看图，让用户能对所有节点有直观的感受，可以清晰地观察节点与其邻居之间的直接关系；
- 有效：信息传达有重点，克制不冗余，避免信息过载；

​	综上，我们选择了基于JavaScript 的开源可视化图表库**Apache Echarts**作为本项目的可视化工具。在此基础之上，我们认为本项目需要实现的第一个功能点是**支持对不同仓库的协作网络图通过时间进行索引**，用户可以通过自定义仓库名称、年份、月份等参数调取需要的网络图。其次，由于数据集中，节点与边存在丰富的属性信息，如果将全部属性展现的图中，则会导致生成的图异常臃肿，不便于用户观察；而如果选择忽略展示这些数据，则会导致部分语义的缺失，容易让用户产生困惑，因此本项目需要实现的第二个功能点是**优化网络图的显示**，即在网络生成时展示一部分具有代表性的信息，如仓库名称、issue编号等，而对于其它的的属性，用户可以将鼠标指针悬浮在该节点或边进行观察。此外，对于一些无法直接从现有数据中获取的、需要进行一些计算得到的信息，我们希望额外设置一些模块进行展示，例如，当用户单击某个节点，将显示该节点关联的所有边的信息；当用户选择某个仓库，显示该仓库的网络图中OpenRank值排名Top-k的节点等。

## 项目文件

项目结构如下所示：

```plaintext
openg
├── data
├── src
│   ├── create_graph.py
│   ├── create_sub_graph.py
│   └── get_graph.py
├── static
│   ├── background.png
│   ├── draw.js
│   ├── func.js
│   ├── jquery-3.7.0.min.js
│   └── logo.png
├── templates
│   └── index.html
└── main.py
```

其中`data/`目录下存放获取数据集的脚本；`src/`目录下存放建库与查询代码；`static/`目录下包含前端所需静态文件以及前端交互代码；`templates/`目录下存放html模板代码；`main.py`为项目入口文件。

## 工作内容

### 数据集准备

​	在数据集准备阶段，通过`wget`命令拉取了`alibaba/canal,alibaba/druid,apache/pulsar`在内的多个仓库从2020年至2023年产生的协作数据，具体参数如下：

|    参数    |  数值  |
| :--------: | :----: |
|  仓库数量  |   12   |
|   节点数   | 56000  |
|    边数    | 389816 |
| 数据集大小 | 21.4MB |

### 图数据库Neo4j部署及查询语句设计

​	本项目在单机环境下部署了图数据库Neo4j，使用py2neo框架与之交互，并基于已知的节点和边的属性构建了相应的数据模型，建库代码如下所示：

~~~python
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
~~~

相应的查询代码如下：

```python
def get_graph(name, year, month):
    cypher = "MATCH (a)-[l]-(b) WHERE a.repository='{}' AND a.year='{}' AND a.month='{}' RETURN a,b,l".format(
        name, year, month)
    graph = Graph('http://localhost:7474/', password='12345678', name='neo4j')
    result = graph.run(cypher).to_data_frame()
    result = dataframe2json(result)
    return result
```

### 可视化工具Apache Echarts使用

本项目使用了Apache Echarts中的**WebKit模块关系依赖图**作为模板，该模板支持对节点的拖动，以及根据节点类型进行过滤等功能。

![](https://github.com/iWYZ-666/openg/blob/main/img/pic1.png?raw=true)

在此基础之上，添加了指针悬浮事件与双击事件，代码如下：

```javascript
var onGraphDataLoaded = graph => {
    var chart = echarts.init(chartDom)
    setLeaderboard(graph);
    let nodes = graph.nodes.map(node => {
        return {
            id: node.id,
            name: genName(node),
            symbolSize: Math.log(node.v + 1) * 6,
            value: node.v,
            category: typeMap.get(node.c),
        };
    });

    let links = graph.links.map(link => {
        return {
            source: link.s,
            target: link.t,
            value: link.w,
        };
    });
    let categories = Array.from(typeMap.values());
    option = {
        title: {
            text: `OpenRank Graphs`,
            top: 'bottom',
            left: 'center'
        },
        legend: [
            {
                data: categories,
            }
        ],
        tooltip: {
            trigger: 'item',
        },
        series: [
            {
                name: 'Collaborative graph',
                type: 'graph',
                layout: 'force',
                nodes,
                links,
                categories: categories.map(c => {
                    return {name: c};
                }),
                roam: true,
                label: {
                    position: 'right',
                    show: true,
                },
                force: {
                    layoutAnimation: false,
                    repulsion: 300
                },
            }
        ]
    };
    chart.setOption(option);
    chart.on('dblclick', function (params) {
        setDetails(bigData, bigData.nodes.find(i => i.id === params.data.id));
    });
}
```

### 前端界面设计

~~~html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <script src="../static/jquery-3.7.0.min.js"></script>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css"
          integrity="sha384-xOolHFLEh07PJGoPkLv1IbcEPTNtaed2xpHsD9ESMhqIYd0nLMwNLD69Npy4HI+N" crossorigin="anonymous">
<!--    <script src="https://cdn.jsdelivr.net/npm/jquery@3.5.1/dist/jquery.slim.min.js" integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous"></script>-->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-Fy6S3B9q64WdZWQUiU+q4/2Lc9npb8tCaSX9FK7E8HnRr0Jz8D6OP9dO5Vg3Q9ct" crossorigin="anonymous"></script>
    <title>Home</title>
    <script src=" https://cdn.jsdelivr.net/npm/echarts@5.4.2/dist/echarts.min.js"></script>


    <style>
        body {
            background-image: url('../static/background.png');
            background-repeat: no-repeat;
            background-size: cover;
        }

        html {
            font-size: 16px;
        }

        .custom-select {
            appearance: none;
            -webkit-appearance: none;
            -moz-appearance: none;
            background-color: #f8f9fa;
            /* border: 1px solid #ced4da;
            padding: 10px; */
            border-radius: 4px;
            width: 200px;
            font-size: 16px;
            color: #495057;
            cursor: pointer;
        }

        .custom-select:focus {
            outline: none;
            box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
        }

    </style>
</head>
<body>

<div>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <div class="container-fluid">
        <a class="navbar-brand" href="#" >
          <img src="../static/logo.png" alt="Logo" style="width: 75px; height: auto;">
        </a>
        <div class="col-md-8 mx-auto" style="color:white;float:left" >
          <form onsubmit="return false;">
              <label style="letter-spacing: 20px; text-indent: 20px;">

                  <select id="repository" onchange="getYears()" class="custom-select">
                      <option value="0">--请选择一个仓库--</option>
                      {% for x in names %}
                        <option value="{{ x }}">{{ x }}</option>
                      {% endfor %}
                  </select>
              </label>
              <label style="letter-spacing: 20px; text-indent: 20px;">

                  <!-- <select id="year" onchange="getMonths()">

                  </select> -->
                  <select id="year" class="custom-select" onchange="getMonths()">
                    <!-- 这是测试数据 后面把names改成year？ -->
                    <!-- <option selected>选择项</option>
                    <option value="1">选项1</option>
                    <option value="2">选项2</option>
                    <option value="3">选项3</option> -->
                    <option selected>--请选择年份--</option>

                  </select>
              </label>



              <label style="letter-spacing: 20px; text-indent: 20px;">

                  <!-- <select id="month">

                  </select> -->
                  <select id="month" class="custom-select">
                    <!-- 这是测试数据 后面把names改成year？ -->
                    <!-- <option selected>选择项</option>
                    <option value="1">选项1</option>
                    <option value="2">选项2</option>
                    <option value="3">选项3</option> -->
                    <option selected>--请选择月份--</option>

                  </select>
              </label>

              <label style="letter-spacing: 20px; text-indent: 20px;">
                 <button type="button" class="btn btn-primary" onclick="sendPost()">确定</button>
                  <!-- <input type="button" onclick="sendPost()"> -->
              </label>
          </form>
      </div>
      </div>
    </nav>

      <br>
    <div class="container-fluid">
      <div class="row">
        <div class="col-md-7 mx-auto">
          <div id="main" style="width: 900px;height:900px;"></div>
        </div>
        <div class="col-md-2.6 mx-auto">
          <div id="details" class="bordered">
            <div class="card">
              <div class="card-body">
                <h5 class="card-title" style="text-align: center;">Details</h5>
                <!-- <p class="card-text">With supporting text below as a natural lead-in to additional content.</p> -->
              </div>
            </div>
            <div id="details_div" class="scrollit">
            <!-- <table id="details_table" class="table table-striped"></table> -->
            <table id="details_table" class="table">
              <thead>
                <tr>
                  <th scope="col">From</th>
                  <th scope="col">Ratio</th>
                  <th scope="col">Value</th>
                  <th scope="col">OpenRank</th>
                </tr>
              </thead>
            </table>
            </div>
        </div>
        </div>
        <div class="col-md-2.6 mx-auto">
          <div id="main_1" class="bordered">
            <div id="graph" class="bordered"></div>
            <div id="control" class="bordered">
            <div id="list" class="bordered">
                <!-- <div id="title">
                <h2>Leaderboard</h2>
                </div> -->
                <div id="leaderboard_div">
                <div class="card">
                  <div class="card-body">
                    <h5 class="card-title" style="text-align: center;">Leaderboard</h5>
                  </div>
                </div>
                <table id="leaderboard_table" class="table"> </table>
                </div>
            </div>
            </div>
          </div>
        </div>
      </div>
    </div>
</div>
<script src="../static/draw.js"></script>
<script src="../static/func.js"></script>

</body>
</html>
~~~

## 结果

- 整体界面展示

![](https://github.com/iWYZ-666/openg/blob/main/img/主界面.png?raw=true)

- 根据仓库名、日期检索相应的协作网络


![](https://github.com/iWYZ-666/openg/blob/main/img/pic2.png?raw=true)

- 指针悬浮事件(属性信息展示)


![](https://github.com/iWYZ-666/openg/blob/main/img/悬浮.png?raw=true)

- 指针点击事件(关联边信息展示)


![](https://github.com/iWYZ-666/openg/blob/main/img/双击.png?raw=true)