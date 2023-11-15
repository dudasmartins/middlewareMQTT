import re
import paho.mqtt.client as mqtt
import psycopg2
from datetime import datetime
import rpyc
from cryptography.fernet import Fernet, InvalidToken
from cassandra.cluster import Cluster

# Conexão banco de dados
cluster = Cluster(['172.19.0.2'])  # endereço servidor cassandra
session = cluster.connect('data')  # "keyspace" banco de dados

#conexão com o mqtt-server

broker_mqtt = "localhost"
port_mqtt = 1883

portRPC = 18861

chave_criptografia = b'9i7e0z0FtQNjj85riGhBy7ZAdxTs8gPSg7BFIUrvka8='
cipher = Fernet(chave_criptografia)

##callback quando o cliente MQTT se conecta ao servidor MQTT
def on_connect(client, userdata, flags, rc):
    client.subscribe("/saude")

def on_message(client, userdata, msg):
    dado = msg.payload.decode()
    dado_descriptografado = decrypt_msg(dado)

    if dado_descriptografado:
        print("Dados recebidos:", dado_descriptografado)

        salvar_dados_cassandra(*map(float, dado_descriptografado.split(',')))


def decrypt_msg(msg):
    try:
        dado_descriptografado = cipher.decrypt(msg.encode()).decode()
        return dado_descriptografado
    except InvalidToken:
        print("Erro na descriptografia. Mensagem descartada.")
        return None

def salvar_dados_cassandra(saturacao, insulina, pressao_sistolica, pressao_diastolica, data_atual):
    query = f"""
    INSERT INTO old_people (saturacao, insulina, pressao_sistolica, pressao_diastolica, data_hora)
    VALUES ({saturacao}, {insulina}, {pressao_sistolica}, {pressao_diastolica}, '{data_atual}');
    """

    try:
        session.execute(query)
        print("Dados salvos no Cassandra.")
    except Exception as e:
        print(f"Erro ao salvar dados no Cassandra: {e}")



#callback quando uma mensagem é recebia no tópico "/saude"
# def on_message(client, userdata, msg):

# def publica_dados_idosos_atuador(saturacao, insulina, pressao_sistolica, pressao_diastolica, data_atual):
#     #ativar o atuador com base nos dados do idoso
#     if(
#         float(saturacao) < 95.0
#         or float(insulina) > 130.0
#         or int(pressao_sistolica) > 120
#         or int(pressao_diastolica) > 80
#     ):
#         print("atuador ativado: dados fora dos limites desejados")
#         dados_enviar = f"{saturacao},{insulina},{pressao_sistolica},{pressao_diastolica},{data_atual}"
#         client.publish("/ativo_idoso", dados_enviar)
#     else:
#         print("Dados dentro dos limites desejados. Atuador não ativado.")

# Configuração do cliente MQTT


client = mqtt.Client("Gerador_Dados")
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_mqtt, port_mqtt)

client.loop_forever()