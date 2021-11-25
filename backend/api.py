import flask
import json
import mariadb
import mysql.connector as database
from flask import request, jsonify
from flask_cors import CORS

connection = database.connect(
    user="root",
    password="admin",
    host='127.0.0.1',
    database="innovatieplatform")
cur = connection.cursor()

# create the flask app
app = flask.Flask(__name__)
app.config["DEBUG"] = True
CORS(app)


@app.route('/api/project/<projectid>', methods=['PUT'])
def index2(projectid):
    cur.execute("UPDATE projects SET isarchived = NOT isarchived WHERE projectid = " + projectid)
    connection.commit()
    # return the results!
    return jsonify({"success": True})


@app.route('/api/projects', methods=['GET'])
def index():
    cur.execute("select * from projects")
    # serialize results into JSON
    row_headers = [x[0] for x in cur.description]
    rv = cur.fetchall()
    json_data = []
    for result in rv:
        json_data.append(dict(zip(row_headers, result)))

    # return the results!
    return json.dumps(json_data, indent=4, sort_keys=True, default=str)


@app.route('/api/project/<projectid>', methods=['DELETE'])
def index3(projectid):
    cur.execute("DELETE FROM projects WHERE projectid =" + projectid)
    connection.commit()
    # return the results!
    return jsonify({"success": True})


app.run(host='192.168.0.123', port=5000, debug=False)
