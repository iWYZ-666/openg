import duckdb
import json
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from src import util

# config
config = json.loads(open(util.get_rel_path("conf"), "r").read())
DB_PATH = util.get_rel_path(config["db_path"])
DB_NAME = config["db_name"]

table_dict = {"r": "repositories", "u": "users", "i": "issues", "p": "prs"}
link_dict = {"ru": "repository_user", "ri": "repository_issue",
             "rp": "repository_pr", "ui": "user_issue", "up": "user_pr"}

conn = duckdb.connect(DB_PATH + DB_NAME)
for table in table_dict.values():
    print(table)
    print(conn.execute(f"SELECT * FROM {table}").fetchall())
for table in link_dict.values():
    print(table)
    print(conn.execute(f"SELECT * FROM {table}").fetchall())
