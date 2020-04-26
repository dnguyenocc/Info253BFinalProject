from flask import Flask, request, Response
import json

app = Flask(__name__)

import MySQLdb

cursor = None
db = None


def get_db_connection():
    global cursor
    global db

    if not cursor:
        db = MySQLdb.connect("some-mysql", "root", "my-secret-pw", "demo")
        cursor = db.cursor()

    return cursor


@app.route('/v1/folders', methods=['POST'])
def create_folder():
    data = request.get_json()
    sql = f"INSERT INTO folders (title) VALUES (%s)"
    if "name" in data:
        name = data["name"]
        cursor = get_db_connection()
        cursor.execute(sql, [name])
        cursor.execute(f"SELECT id FROM folders WHERE title=(%s)", [data["name"]])
        assigned_id = cursor.fetchone()[0]
        resp = Response(json.dumps(assigned_id), status=201, mimetype='application/json')
        db.commit()
    else:
        resp = Response("Error", status=400)
    return resp


@app.route('/v1/folders/<id>/add_document', methods=['POST'])
def add_doc_to_folder(id):
    data = request.get_json()
    sql = f"INSERT INTO contains (document_id, folder_id) VALUES (%s, %s)"
    if "document_id" in data:
        doc_id = data["document_id"]
        cursor = get_db_connection()
        cursor.execute(sql, [doc_id, id])
        resp = Response(json.dumps("Success"), status=201, mimetype='application/json')
        db.commit()
    else:
        resp = Response("Error", status=400)
    return resp


@app.route('/v1/folders/<id>', methods=['GET'])
def get_documents(id):
    sql = f"SELECT * FROM contains WHERE folder_id=(%s)"
    cursor = get_db_connection()
    cursor.execute(sql, [id])
    data = cursor.fetchall()
    doc_ids = list()
    for row in data:
        doc_ids.append(row[1])
    return Response(json.dumps(doc_ids), status=200, mimetype='application/json')


@app.route('/v1/folders/<id>', methods=['PUT'])
def edit_folder(id):
    data = request.get_json()
    sql = f"UPDATE folders SET title=(%s) WHERE id=(%s)"
    if "name" in data:
        new_name = data["name"]
        cursor = get_db_connection()
        cursor.execute(sql, [new_name, id])
        resp = Response(json.dumps("Success"), status=201, mimetype='application/json')
        db.commit()
    else:
        resp = Response("Error", status=400)
    return resp


@app.route('/v1/folders/<id>', methods=['DELETE'])
def delete_folder(id):
    sql2 = f"DELETE FROM folders WHERE id=(%s)"
    sql1 = f"DELETE FROM contains WHERE folder_id=(%s)"
    cursor = get_db_connection()
    cursor.execute(sql1, [id])
    cursor.execute(sql2, [id])
    db.commit()
    return Response(json.dumps("Success"), status=201, mimetype='application/json')


@app.route('/v1/folders', methods=['GET'])
def get_folders():
    sql = f"SELECT * FROM folders"
    cursor = get_db_connection()
    cursor.execute(sql)
    data = cursor.fetchall()
    folders_list = list()
    for row in data:
        folders_list.append({"name": row[1], "id": row[0]})
    return Response(json.dumps({"result": folders_list}), status=200, mimetype='application/json')