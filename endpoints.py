from flask import Flask
from flask_cors import CORS
from api import utils

app = Flask(__name__)
PORT = 5000
DEBUG = True
CORS(app)


@app.errorhandler(404)
def not_found(error):
    return "<h1>Not Found</h1>" \
           f"<p>{error}</p>"


@app.route("/", methods=["GET"])
def hello():
    return "<h1>Ingresa la palabra a buscar en la barra de direcciones</h1>" \
            "<p>https://graphora.herokuapp.com/graph/'Palabra'</p>" \
            "<h1>Ingresa letras para encontrar posibles resultados</h1>" \
            "<p>https://graphora.herokuapp.com/search/'Letras'</p>" \
            "<h1>Ingresa la palabra a buscar en la barra de direcciones para obtener las propiedades de la relación</h1>" \
            "<p>https://graphora.herokuapp.com/table/'Palabra'</p>"


@app.route("/graph/<word>", methods=["GET"])
def graph(word):
    result = utils.getGraph(word)
    return utils.validation(result)


@app.route("/search/<letters>", methods=["GET"])
def search(letters):
    return utils.getStimulus(letters)


@app.route("/table/<word>", methods=["GET"])
def table(word):
    tableJSON = utils.getTable(word)
    return utils.validation(tableJSON)
