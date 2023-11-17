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
    client.subscribe("/nivel_oxigenio")

def on_message(client, userdata, msg):
    dado = msg.payload.decode()
    dado_descriptografado = decrypt_msg(dado)


def salvar_dados_cassandra(dados):
    nivel_oxigenio = int(dados.split(',')[0])
    data_atual = dados.split(',')[1]

    publica_nivel_oxigenio_atuador(nivel_oxigenio, data_atual)

    try:
        session.execute(query)
        print("Dados salvos no Cassandra.")
    except Exception as e:
        print(f"Erro ao salvar dados no Cassandra: {e}")


def publica_nivel_oxigenio_atuador(nivel_oxigenio, data_atual):
    if (nivel_oxigenio < 70()):
        print("Enviado: " + str(nivel_oxigenio))
        dados_enviar = f'{str(nivel_oxigenio)},{data_atual}'
        client.publish("", dados_enviar)
    else:
        print('Não é necessário publicar')

    # Configuração do cliente MQTT


client = mqtt.Client()
client.connect(broker_mqtt, port_mqtt)
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish
client.loop_forever()