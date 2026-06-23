from flask import Flask,request,jsonify
from flask_cors import CORS 
import sqlite3
import os

app = Flask(__name__)
CORS(app)

tasks_db = 'task_db.db'

def init_db():
    conn = sqlite3.connect(tasks_db)
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        task_text TEXT NOT NULL
    )
    ''')
    conn.commit()
    cur.close()
    return conn

@app.route('/',methods=['POST'])
def get_task():
    data = request.get_json()
    task = data.get('task_text')
    conn = init_db()
    cur = conn.cursor()
    cur.execute('''
    INSERT INTO tasks (task_text) VALUES (?)
    ''',(task,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message':'task added successfuly'})

@app.route('/tasks',methods=['GET'])
def post_tesks():
    conn = init_db()
    cur = conn.cursor()
    cur.execute('''
    SELECT * FROM tasks
    ''')
    rows = cur.fetchall()
    cur.close()
    conn.close()

    tasks_list = [ { "task_text": r[0] } for r in rows]
    return jsonify({ "tasks": tasks_list})

if __name__ == '__main__':
    port = int(os.environ.get('PORT',8000))
    app.run(host='0.0.0.0',debug=True,port=port)