from flask import Flask, request, Response
import json
app = Flask(__name__)

import MySQLdb

cursor = None
def get_db_connection():
    global cursor

    if not cursor:
        db = MySQLdb.connect("some-mysql", "root", "my-secret-pw", "demo")
        cursor = db.cursor()

    return cursor


@app.route('/v1/documents', methods = ['POST'])
def create_document():
    data = request.get_json()
    sql = f"INSERT INTO documents (title, content) VALUES (%s, %s)"
    if "title" in data:
        title = data["title"]
        content = data["content"]
        cursor = get_db_connection()
        cursor.execute(sql, [title, content])
        resp = Response(json.dumps("Success"), status=201, mimetype='application/json')
    else:
        status_code = 400
        resp = Response("Error", status=400)
    return resp

