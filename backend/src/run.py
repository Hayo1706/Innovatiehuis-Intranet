from services import app
import connexion

if __name__ == "__main__":
    app.app.run(host='127.0.0.1', debug=True)
