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

@app.route('/v1/folders', methods = ['POST'])
def create_document():
    data = request.get_json()
    sql = f"INSERT INTO folders (name) VALUES (%s)"
    if "name" in data:
        name = data["name"]
        cursor = get_db_connection()
        cursor.execute(sql, [name])
        resp = Response(json.dumps("Success"), status=201, mimetype='application/json')
    else:
        status_code = 400
        resp = Response("Error", status=400)
    return resp


