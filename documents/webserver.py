from flask import Flask, request, Response
import file_worker
import json
app = Flask(__name__)
import requests
import MySQLdb
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions

#Azure API
api_key = "b4831cbb0cad4cf2b0e78abbbfda8e5d"
endpoint = "https://info253.cognitiveservices.azure.com/bing/v7.0/spellcheck"
params = {
    'mkt':'en-us',
    'mode':'proof'
    }

headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Ocp-Apim-Subscription-Key': api_key,
    }


#IBM API

authenticator = IAMAuthenticator('GO9rlymCQcmv9QP7yZW2_YVGTi1v9C7tZnVK_1_SyA52')
natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2019-07-12',
    authenticator=authenticator
)

natural_language_understanding.set_service_url('https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/46f58ada-84c3-4c16-bceb-3d0ee1cae13f')

# cursor = None
# def get_db_connection():
#     global cursor
#
#     if not cursor:
#         db = MySQLdb.connect("some-mysql", "root", "my-secret-pw", "demo")
#         cursor = db.cursor()
#
#     return cursor

conn = None
def get_db_connection():
    global conn
    if not conn:
        conn = MySQLdb.connect("some-mysql", "root", "my-secret-pw", "demo")
    return conn

@app.route('/v1/documents', methods=['POST'])
def create_document():
    conn = get_db_connection()
    cursor = conn.cursor()
    data = request.get_json()

    # insert into documents table
    title = data["title"]
    content = data["content"]
    sql = f"INSERT INTO documents (title, content) VALUES (%s, %s);"
    
    cursor.execute(sql, [title, content])
    new_document_id = cursor.lastrowid

    # insert into relationhip
    folder_id = 1
    if "folder_id" in data:
        folder_id = data["folder_id"]

    sql = f"INSERT INTO contains (document_id, folder_id) VALUES (%s, %s);"
    cursor.execute(sql, [new_document_id, folder_id])

    conn.commit()

    resp = Response(json.dumps({"id": new_document_id}), status=201, mimetype='application/json')
    return resp

# @app.route('/v1/documents', methods=['POST'])
# def create_document():
#     data = request.get_json()

#     if data:
#         conn = get_db_connection()
#         title = data["title"]
#         content = data["content"]
#         if "folder_id" in data:
#             resp = Document.create(conn, title, content, data["folder_id"])
#         else:
#             resp = Document.create(conn, title, content)
#     else:
#         status_code = 400
#         resp = Response("Error", status=status_code)
#     return resp


##Get all documents
@app.route('/v1/documents', methods=['GET'])
def get_all_documents():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, title FROM documents")
    data = cursor.fetchall()
    response_msg = list()
    for row in data:
        response_msg_link = dict()
        response_msg_link["id"] = row[0]
        response_msg_link["title"] = row[1]
        # response_msg_link["last_modified"] = str(row[2])
        response_msg.append(response_msg_link)
    response = {"documents" : response_msg}

    return json.dumps(response), 200


#2. Get a document content
@app.route('/v1/documents/<id>', methods=['GET'])
def get_content(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    sql_get_query = "SELECT title, content FROM documents WHERE id = %s"
    rows_count = cursor.execute(sql_get_query, [id])
    if rows_count > 0:
        data = cursor.fetchall()
    else:
        response = {'error': "There is no document at that id"}
        return json.dumps(response), 404
    response = dict()

    for row in data:
        response["title"] = row[0]
        response['content'] = row[1]
        return json.dumps(response), 200


##3. Get a spell check for a document
@app.route('/v1/documents/<id>/spell_check', methods=['GET'])
def spell_check(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    sql_get_query = "SELECT content from documents WHERE id = %s"
    rows = cursor.execute(sql_get_query, [id])
    if rows > 0:
        data = cursor.fetchall()
    else:
        response = {'error': "There is no document at that id"}
        return json.dumps(response), 404

    data = {'text': str(data[0][0])}
    response_api = requests.post(endpoint, headers=headers, params=params, data=data)
    json_response = response_api.json()
    return json.dumps(json_response, indent=4)


#4. Word counts
@app.route('/v1/documents/<id>/word_count/<stop_word>', methods=['GET'])
def process_a_document(id, stop_word):
    conn = get_db_connection()
    cursor = conn.cursor()

    sql_get_query = "SELECT content from documents WHERE id = %s"
    rows = cursor.execute(sql_get_query, [id])
    if rows > 0:
        data = cursor.fetchall()
        content = str(data[0][0])
        file_w = file_worker.FileWorker(content, stop_word)
        top_25_words = file_w.get_top_25_words()
        column = ['id', 'top_25_words']
        res_data = dict(zip(column, [id, top_25_words]))
        resp = Response(json.dumps(res_data), status=201, mimetype='application/json')
    else:
        response = {'error': "There is no document at that id"}
        resp = json.dumps(response), 404

    return resp


#5. Change Document
@app.route('/v1/documents/<id>', methods=['PUT'])
def put(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    data = request.get_json()
    new_title = data['title']
    new_content = data['content']
    new_folder_id = data['folder_id']

    sql_get_query = "SELECT * from documents WHERE id = %s"
    row_count = cursor.execute(sql_get_query, [id])
    if row_count > 0:
        sql_put_query = "UPDATE documents SET title = %s, content = %s WHERE id = %s"
        cursor.execute(sql_put_query, [new_title, new_content, id])

        #Change folder ID
        sql_put_query = "UPDATE contains SET folder_id = %s WHERE document_id = %s"
        cursor.execute(sql_put_query, [new_folder_id, id])
        resp =  json.dumps("Success"), 204
    else:
        response = {'error': 'There is no document at that id'}
        resp = json.dumps(response), 404

    conn.commit()
    return resp


#6. Delete document
@app.route('/v1/documents/<id>', methods = ['DELETE'])
def delete_document(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    #delete in relationship
    sql_delete_query = "DELETE FROM contains WHERE document_id = %s"
    cursor.execute(sql_delete_query, [id])

    sql_delete_query = "DELETE FROM documents WHERE id = %s"
    cursor.execute(sql_delete_query, [id])
    

    conn.commit()
    return json.dumps("Success"), 204


#8 NLP using IBM API
#https://www.ibm.com/cloud/watson-natural-language-understanding
@app.route('/v1/documents/<id>/analyze', methods=['GET'])
def analyze(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    sql_get_query = "SELECT content from documents WHERE id = %s"
    rows = cursor.execute(sql_get_query, [id])
    if rows > 0:
        data = cursor.fetchall()
    else:
        response = {'error': "There is no document at that id"}
        return json.dumps(response), 404

    content = {'text': str(data[0][0])}
    response = natural_language_understanding.analyze(
        text=content['text'],
        features=Features(
            entities=EntitiesOptions(emotion=True, sentiment=True, limit=2),
            keywords=KeywordsOptions(emotion=True, sentiment=True,
                                     limit=2))).get_result()
    return json.dumps(response, indent=4)
