import connexion

# create the flask app
# Create the application instance
app = connexion.App(__name__, specification_dir="./")

# Read the swagger.yml file to configure the endpoints
app.add_api("swagger.yml")

if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True)
