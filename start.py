#encoding=utf-8
'''
简单demo
'''
from flask import Flask
from flask import request
from flask import render_template
import json,datetime,sqlite3
app = Flask(__name__)
sqlpath="action.db"

def get_action(start_id):
    conn=sqlite3.connect(sqlpath)
    c = conn.cursor()
    sql = "SELECT * FROM action where id < ? order by id desc limit 4"
    cursor = c.execute(sql, (start_id,) )
    data = ''
    min_id = start_id
    for row in cursor:
        row_id, user_id, op_type, act_user_id, act_user_name, repo_id, repo_user_name, repo_name, ref_name, is_private, content, created_unix = row
        min_id = min(start_id, row_id)
        date = datetime.datetime.fromtimestamp(created_unix)
        if op_type == 4:
            data += render_template("star.tpl", act_user_name=act_user_name, repo_name=repo_name, date=date)
        elif op_type == 3:
            try:
                content_param = json.loads(str(content))
            except:
                content_param = {}
            data += render_template("commit.tpl", act_user_name=act_user_name, repo_name=repo_name, commit=content_param["Commits"][0]["Sha1"], date=date)
        elif op_type == 1:
            data += render_template("create.tpl", act_user_name=act_user_name, repo_name=repo_name, date=date)
        elif op_type == 5:
            try:
                content_param = json.loads(str(content))
            except:
                content_param = {}
            data += render_template("fork.tpl", act_user_name=act_user_name, repo_name=repo_name, fork_name=content_param["ForkName"], date=date)
        else:
           data += render_template("follow.tpl", act_user_name=act_user_name, repo_name=repo_name, repo_user_name=repo_user_name, date=date)
    if min_id > 1:
        data += render_template("page.tpl", start_id=min_id)
    return data

@app.route('/')
def index():
    content = get_action(99999)
    return render_template("index.tpl", content=content)
@app.route('/get')
def get():
    start_id = request.args.get('start_id', 99999)
    content = get_action(start_id)
    return content
