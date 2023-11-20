<p align="center"><img src="https://github.com/iWYZ-666/openg/blob/main/img/logo.png?raw=true" style="width:25%;" /></p>

本项目为OpenSODA | OpenDigger 开源软件生态数据分析挖掘平台挑战赛的参赛项目，赛题为**W3：开源协作网络可视化**，队名为**新奥尔良鹈鹕**，队伍成员包括[胡展翊](https://github.com/Rainysponge)、[卫涛](https://github.com/JackWeiw)、[程奂仑](https://github.com/iWYZ-666)、[刘雨石](https://github.com/Liuyushiii)。

随着开源协作从单纯的 Git 代码协作扩大为基于 Issue、Pull Request、Discussion、Follow 等具有 GitHub 特性的多维协作，协作体现出的个体间联系形成了极为复杂的网络，通过对这种网络进行构造、分析和可视化展现，能够帮助人们更好地洞察开源世界。openg 面向海量的项目协作网络数据，构建了通用的协作网络可视化平台，支持用户自定义的数据检索，结合多种可视化技术深入挖掘潜藏在协作网络中的知识，并将分析由单一网络扩展至多个网络，从项目间的内在联系中获取洞见，为开源世界的持续、健康发展贡献力量。



## 环境准备

输入以下命令安装第三方python库

~~~bash
pip3 install -r requirements.txt
~~~

使用Docker部署Neo4j

```shell
docker run \
    --publish=7474:7474 --publish=7687:7687 \
    --volume=$HOME/neo4j/data:/data \
    neo4j
```



## 数据准备

输入以下命令获取数据集

~~~bash
python3 src/download_json.py
~~~

输入以下命令将数据导入 Neo4j 与 DuckDB

~~~bash
python3 src/create_graph.py
~~~



## 运行项目

输入如下命令运行本项目：

~~~bash
cd backend && python3 manage.py runserver 0.0.0.0:8000
~~~

在浏览器中输入 `{ip地址}:8000` 即可访问。

<img src="https://github.com/iWYZ-666/openg/blob/main/img/ui.jpeg?raw=true" style="zoom: 50%;" />



## 系统架构

在协作网络数据的可视化上，openg 选用 Echarts 作为统计信息的可视化工具，这主要是因为Apache ECharts 是一款强大的、开源的统计信息可视化工具，支持丰富的图表类型，如折线图、柱状图、饼图、散点图、地图等，以及更高级的统计图表和自定义图表。Apache ECharts易用性强、高度可定制化，以及良好的跨平台性能，并为用户提供了详细的文档和示例，使得即使是非专业开发者也能快速上手，创建出美观且互动性强的数据视图。此外，其灵活的配置项和响应式设计确保可视化在不同设备和分辨率上的兼容性，满足现代数据可视化的需求。而在协作网络的可视化方面，我们则选用 AntV G6 这款专注于图形可视化的引擎，它的主要优势在于为协作网络的复杂可视化需求提供了专业的解决方案。G6 强调易用性和灵活性，支持各种图表类型，如流程图、关系图、树形图等，特别适合于展现复杂的网络关系和层次结构。G6 提供了丰富的交互行为和自定义样式，可以轻松实现节点、边的动态添加、删除或更新，且内置了多种布局算法，帮助用户快速构建出清晰、可交互的网络拓扑图。此外，G6 的性能优化使其能够流畅地处理大规模数据，这对于协作网络的深度分析和数据洞察尤为重要。

<p align="center"><img src="https://github.com/iWYZ-666/openg/blob/main/img/echarts.png?raw=true" style="width: 25%;" /><img src="https://github.com/iWYZ-666/openg/blob/main/img/antv_g6.jpeg?raw=true" style="width: 25%;" /></p>

在数据存储上，openg 选用 neo4j 对规模庞大的协作网络数据进行存储，主要原因在于 neo4j 的灵活性和强大的关系处理能力；它能够高效处理网络中的节点和边的关系，提供深度联接查询和图算法，这对于发现数据中的模式和洞察至关重要。此外，Neo4j 还有一个活跃的开发者社区和丰富的生态系统，提供了大量的工具和库，以支持各种查询和可视化需求，这使得它成为构建和维护大型协作网络的理想选择。针对协作网络数据中的元信息，则选用开源的分析性SQL数据库 DuckDB 进行存储，这主要是因为其卓越的查询性能和易于集成的特点。它为大规模数据集提供了快速的OLAP（在线分析处理）功能，这意味着可以迅速执行复杂的分析查询。它的轻量级架构使得它可以作为嵌入式数据库直接集成到现有应用中，而无需复杂的配置。此外，DuckDB支持标准SQL，使得开发者能够使用熟悉的查询语言来处理和分析协作网络中的元数据。

<p align="center"><img src="https://github.com/iWYZ-666/openg/blob/main/img/neo4j.png?raw=true" style="width: 12.5%;" /> &nbsp <img src="https://github.com/iWYZ-666/openg/blob/main/img/duckdb.png?raw=true" style="width: 25%;" /></p>

