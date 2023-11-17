import rpyc
import random
import json
from flask import Flask, request, jsonify
import time

app = Flask(__name__)

porta_control1 = 18861

# Buscar os dados
@app.route('/', methods=['GET'])
def buscar_dados():
    try:
        # Conexão com o controlador 1
        proxy_control = rpyc.connect('localhost', porta_control1, config={'allow_public_attrs': True, 'sync_request_timeout': 1})
    except ConnectionRefusedError as e:
        return jsonify({"sucesso": False, "erro": "Controlador indisponível"})

    # Obtém dados do controlador
    dados = proxy_control.root.retorna_todos_dados()
    json_data = json.dumps([{'nivel_oxigenio': item[0], 'data_atual': item[1]} for item in dados])

    time.sleep(30)

    # return jsonify({"sucesso": True, "dados": json_data})

if __name__ == "__main__":
    app.run(debug=True)
