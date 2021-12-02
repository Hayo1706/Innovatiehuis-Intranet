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
def putProjectArchived(projectid):
    cur.execute("UPDATE projects SET isarchived = NOT isarchived WHERE projectid = " + projectid)
    connection.commit()
    # return the results!
    return jsonify({"success": True})


@app.route('/api/user/<userid>/projects', methods=['GET'])
def getProjectsByUser(userid):
    cur.execute(
        "SELECT * FROM user_has_projects INNER JOIN projects ON user_has_projects.projectid=projects.projectid WHERE userid = " + userid+" AND projects.isarchived = 0")
    # serialize results into JSON
    row_headers = [x[0] for x in cur.description]
    rv = cur.fetchall()
    json_data = []
    for result in rv:
        json_data.append(dict(zip(row_headers, result)))

    # return the results!
    print(json_data)
    return json.dumps(json_data, indent=4, sort_keys=True, default=str)


@app.route('/api/projects', methods=['GET'])
def getProjects():
    cur.execute("select * from projects")
    # serialize results into JSON
    row_headers = [x[0] for x in cur.description]
    rv = cur.fetchall()
    json_data = []
    for result in rv:
        json_data.append(dict(zip(row_headers, result)))


@app.route('/api/project/<projectid>', methods=['DELETE'])
def deleteProject(projectid):
    cur.execute("DELETE FROM projects WHERE projectid = " + projectid)
    connection.commit()
    # return the results!
    return jsonify({"success": True})


@app.route('/api/project/<projectid>/announcements', methods=['GET'])
def getAnnouncements(projectid):
    cur.execute("SELECT announcements.announcementid, announcements.timestamp, announcements.userid, users.firstname, users.lastname, announcements.title, announcements.content FROM announcements JOIN users ON announcements.userid = users.userid WHERE announcements.projectid = " + projectid + " ORDER BY announcements.timestamp DESC")
    # serialize results into JSON
    row_headers = [x[0] for x in cur.description]
    rv = cur.fetchall()
    json_data = []
    for result in rv:
        json_data.append(dict(zip(row_headers, result)))

    # return the results!
    print(json_data)
    return json.dumps(json_data, indent=4, sort_keys=True, default=str)

@app.route('/api/test', methods=['GET'])
def test():
    cur.execute("SELECT * FROM announcement_replies WHERE announcement_replies_id = 3")
    # serialize results into JSON
    row_headers = [x[0] for x in cur.description]
    rv = cur.fetchall()
    json_data = []
    for result in rv:
        json_data.append(dict(zip(row_headers, result)))

    # return the results!
    print(json_data)
    return json.dumps(json_data, indent=4, sort_keys=True, default=str)

@app.route('/api/project/<projectid>/announcements', methods=['POST'])
def postAnnouncement(projectid):
    cur.execute("INSERT INTO announcements (userid, projectid, title, content) VALUES (1, " + projectid + ", 'nieuwe mededeling', 'AAAAAAAAAAAAA.')")
    connection.commit()
    return jsonify({"success": True})



app.run(host='127.0.0.1', port=5000, debug=False)
