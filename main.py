from flask import Flask
from flask_cors import CORS
from apineo4j import apineo4j

app = Flask(__name__)
PORT = 5000
DEBUG = False
CORS(app)


@app.errorhandler(404)
def not_found():
    return "<h1>Not Found</h1>"


@app.route("/", methods=['GET'])
def hello():
    return "<h1>Ingresa la palabra a buscar en la barra de direcciones</h1>" \
           "<p>https://graphora.herokuapp.com/'Palabra'</p>"


@app.route("/graph/<word>", methods=['GET'])
def data(word):
    result = apineo4j.getData(word)

    if result != "[]":
        return result
    else:
        return "<h1>Palabra invalida</h1>"


@app.route("/search", methods=['GET'])
def search():
    stimulus = apineo4j.allStimulus()
    return stimulus


if __name__ == "__main__":
    app.run(port=PORT, debug=DEBUG)
