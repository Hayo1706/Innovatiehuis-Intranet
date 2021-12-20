import connexion
from flask_cors import CORS

app = connexion.App(__name__, specification_dir="./")

# Read the API.yml file to configure the endpoints
app.add_api("API.yml")
CORS(app.app)
if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True)
