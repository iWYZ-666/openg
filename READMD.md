# Openg

## 环境准备

确保环境中安装wget，ruby，python3。

输入如下命令安装第三方python库：

~~~bash
pip install -r requirements.txt
~~~

## 数据准备

输入如下命令获取数据集：

~~~bash
ruby get_json.rb
~~~

输入如下命令建立Neo4j与sqlite数据库：

~~~bash
python src/create_graph.py
~~~

## 运行项目

输入如下命令运行本项目：

~~~bash
python main.py
~~~

在浏览器中访问localhost:5000即可访问。