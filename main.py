from flask import Flask
from flask_cors import CORS
from apineo4j import apineo4j

app = Flask(__name__)
PORT = 5000
DEBUG = False
CORS(app)


@app.errorhandler(404)
def not_found(error):
    return "<h1>Not Found</h1>"


@app.route("/", methods=['GET'])
def hello():
    return "<h1>Ingresa la palabra a buscar en la barra de direcciones</h1><p>https://graphora.herokuapp.com/'Palabra'</p>"


@app.route("/<word>", methods=['GET'])
def getJSON(word):
    data = apineo4j.getData(word)
    
    if data != "[]":
        return data
    else:
        return "<h1>Palabra invalida</h1>"


if __name__ == "__main__":
    app.run(port=PORT, debug=DEBUG)
