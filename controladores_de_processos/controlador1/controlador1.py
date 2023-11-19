import re
import paho.mqtt.client as mqtt
from datetime import datetime
import rpyc
from cryptography.fernet import Fernet, InvalidToken
from cassandra.cluster import Cluster


#configuração banco cassandra
cluster = Cluster(['cassandra-node1', 'cassandra-node2'])
session = cluster.connect()
db_name = "dados"  # Substitua pelo nome do seu keyspace
table_name = "dados_idosos"

session.set_keyspace(db_name)

session.execute("""
    CREATE KEYSPACE IF NOT EXISTS %s
    WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 3 }
""" % db_name)

session.execute("""
    CREATE TABLE IF NOT EXISTS %s (
        id UUID PRIMARY KEY,
        nivel_oxigenio INT,
        data_atual TIMESTAMP
    )
""" % table_name)

# Conexão com o mqtt-server
broker_mqtt = "localhost"
port_mqtt = 1883

portRPC = 18861

chave_criptografia = b'9i7e0z0FtQNjj85riGhBy7ZAdxTs8gPSg7BFIUrvka8='
cipher = Fernet(chave_criptografia)

## Callback quando o cliente MQTT se conecta ao servidor MQTT
def on_connect(client, userdata, flags, rc):
    client.subscribe("/nivel_oxigenio")

def on_message(client, userdata, msg):
    dado = msg.payload.decode()
    dado_descriptografado = decrypt_msg(dado)

##################CRIPTOGRAFIA##################

def decrypt_msg(dado):
    chave_criptografia = b'9i7e0z0FtQNjj85riGhBy7ZAdxTs8gPSg7BFIUrvka8='.encode()
    cipher = Fernet(chave_criptografia)

    try:
        dado_decrypt = cipher.decrypt(dado).decode()

        if(verifica_padrao_crypto(dado_decrypt)):
            return dado_decrypt

        else:
            return False
    except InvalidToken:
        print('Token não reconhecido')

def verifica_padrao_crypto(data):
    padrao = r'^\d+,\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$'
    correspondencia = re.match(padrao, data)
    return bool(correspondencia)

##################SALVAR NO BANCO DE DADOS##################

def salvar_dados_cassandra(dados):
    nivel_oxigenio = int(dados.split(',')[0])
    data_atual = dados.split(',')[1]

    publica_nivel_oxigenio_atuador(nivel_oxigenio, data_atual)

    try:
        # Gera um UUID único para cada registro
        id_unico = uuid.uuid4()

        # Insere os dados na tabela
        session.execute("""
            INSERT INTO %s (id, nivel_oxigenio, data_atual)
            VALUES (%s, %s, %s)
        """ % (table_name, id_unico, nivel_oxigenio, data_atual))

        print("Dados salvos no banco de dados.")
    except Exception as e:
        print(f"Erro ao salvar dados: {e}")

##################PUBLICA DADOS NO ATUADOR##################

def publica_nivel_oxigenio_atuador(nivel_oxigenio, data_atual):
    if (nivel_oxigenio < 70):
        print("Enviado: " + str(nivel_oxigenio))
        dados_enviar = f'{str(nivel_oxigenio)},{data_atual}'
        client.publish("", dados_enviar)
    else:
        print('Não é necessário publicar')

##################VERIFICAR CONEXÃO BANCO DE DADOS##################

# def verificar_conexao_cassandra():
    # try:
    #     cluster = Cluster(['cassandra-node1', 'cassandra-node2'])
    #     session = cluster.connect()

    #     keyspace = 'dados'

    #     # Execute uma consulta simples para verificar a conexão
    #     rows = session.execute('SELECT cluster_name FROM system.local')

    #     # Verificar se a consulta foi bem-sucedida
    #     for row in rows:
    #         cluster_name = row.cluster_name
    #         print(f'Conexão com o Cassandra está ativa. Cluster: {cluster_name}')
    #         return True

    # except Exception as e:
    #     print(f'Erro ao conectar ao Cassandra: {e}')
    #     return False

    # finally:
    #     # Sempre feche a conexão no bloco finally para evitar vazamentos
    #     cluster.shutdown()

##################SINCRONIZA BANCO DE DADOS##################

def verifica_sincronizacao_bd():
    pass


client = mqtt.Client()
client.connect(broker_mqtt, port_mqtt)
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish
client.loop_forever()