import rpyc
import random
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

porta_control1 = 18861

# porta_controlador1 = 18861

#buscar os dados
@app.route('/', method=['GET'])
def buscar_dados():
    try:
        #conexão com o controlador 1
        proxy_control = rpyc.coonect('localhost', porta_control1, config={'allow_public_attrs': True, 'sync_request_timeout': 1})
    except ConnectionRefusedError as e:
        return jsonify({"sucesso": False, "erro": "Controlador indisponível"})


    # Obtém dadods do controlador
    dados = proxy_control.root.retorna_todos_dados()
    json_data = json.dumps([{'data_hora': item[4], 'saturacao': item[1], 'molhou': item[2]} for item in dados])
    