import re
import paho.mqtt.client as mqtt
from datetime import datetime
import rpyc
from cryptography.fernet import Fernet, InvalidToken
from cassandra.cluster import Cluster
import uuid

class SensorController:
    def __init__(self):
        self.cluster_ips = ['172.20.0.2', '172.20.0.3']
        self.db_name = "dados"
        self.table_name = "dados_idosos"
        self.chave_criptografia = '9i7e0z0FtQNjj85riGhBy7ZAdxTs8gPSg7BFIUrvka8='.encode()
        self.cipher = Fernet(self.chave_criptografia)

        # Configuração do MQTT
        self.broker_mqtt = "localhost"
        self.port_mqtt = 1883

        # Configuração do Cassandra
        self.cluster = Cluster(self.cluster_ips)
        self.session = self.cluster.connect()
        self.session.execute(f"""
            CREATE KEYSPACE IF NOT EXISTS {self.db_name}
            WITH REPLICATION = {{ 'class' : 'SimpleStrategy', 'replication_factor' : 3 }}
        """)
        self.session.set_keyspace(self.db_name)
        self.session.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                id UUID PRIMARY KEY,
                nivel_oxigenio INT,
                data_atual TIMESTAMP
            )
        """)

        # Configuração do MQTT Client
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.connect(self.broker_mqtt, self.port_mqtt)
        self.mqtt_client.loop_start()

    #topico do sensor
    def on_connect(self, client, userdata, flags, rc):
        self.mqtt_client.subscribe("/nivel_oxigenio")

    def on_message(self, client, userdata, msg):
        dado = msg.payload.decode()
        dados_descriptografado = self.decrypt_msg(dado)

        if dados_descriptografado:
            self.salvar_dados_cassandra(dados_descriptografado)
        else:
            print("Dados não reconhecidos.")

    #verificação token 
    def decrypt_msg(self, dado):
        try:
            dado_decrypt = self.cipher.decrypt(dado.encode()).decode()

            if self.verifica_padrao_crypto(dado_decrypt):
                return dado_decrypt
            else:
                return False
        except InvalidToken:
            print('Token não reconhecido')

    #verifica se os dados seguem o padrão de "número,yyyyy,mm-dd hh:mm:ss"
    def verifica_padrao_crypto(self, data):
        padrao = r'^\d+,\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$'
        correspondencia = re.match(padrao, data)
        return bool(correspondencia)

    #se o nivel de oxigenio for inferior a 70, publica no topico de notificacao que está no controlador de processos
    def publica_nivel_oxigenio_atuador(self, nivel_oxigenio, data_atual):
        if nivel_oxigenio < 70:
            print("Enviado: " + str(nivel_oxigenio))
            dados_enviar = f'{str(nivel_oxigenio)},{data_atual}'
            self.mqtt_client.publish("/notificacao", dados_enviar)
        else:
            print('Não é necessário publicar')

    #verifica a conexão dos nós que estão os banco de dados
    def verifica_conexao_nos(self):

        #armazena os IPS na lista
        nodos_ativos = []
        for ip in self.cluster_ips:
            try:
                # Tenta conectar ao nó
                cluster = Cluster([ip])
                session = cluster.connect()
                print(f"Conexão bem-sucedida com o nó {ip}!")
                nodos_ativos.append(ip)

                # Fecha a conexão após a verificação bem-sucedida
                cluster.shutdown()
            except Exception as e:
                print(f"Erro ao conectar ao nó {ip}: {e}")

            if nodos_ativos:
                print(f"Nodos ativos: {nodos_ativos}")
                if len(nodos_ativos) == 2:
                    print("Ambos os nodos estão ativos.")
                elif len(nodos_ativos) == 1:
                    print("Apenas um nó está ativo.")
            else:
                print("Nenhum nó ativo.")

    def salvar_dados_cassandra(self, dados):
        nivel_oxigenio = int(dados.split(',')[0])
        data_atual = dados.split(',')[1]
        data_atual_formatada = f"'{data_atual}'"

        try:
            id_unico = uuid.uuid4()

            #insere os dados na tabela
            self.session.execute(f"""
            INSERT INTO {self.table_name} (id, nivel_oxigenio, data_atual)
            VALUES ({id_unico}, {nivel_oxigenio}, {data_atual_formatada})
            """)
            print("Dados salvos no banco de dados.")
            self.publica_nivel_oxigenio_atuador(nivel_oxigenio, data_atual)
            self.verifica_conexao_nos()

        except Exception as e:
            print(f"Erro ao salvar dados: {e}")

    def verifica_sincronizacao_cluster(self):
        for ip in self.cluster_ips:
            try:
                cluster = Cluster([ip])
                session = cluster.connect()

                # consulta para obter informações sobre o estado do cluster
                query = "SELECT * FROM system.peers;"
                rows = session.execute(query)

                # verifica se todos os nós estão sincronizados (mesmas informações na tabela)
                for row in rows:

                    #verifica o nó selecionado com o primeiro nó na lista
                    if not row.is_alive or not row.is_bootstrapping or row.schema_version != rows[0].schema_version:
                        print(f"Nó {row.peer} não está sincronizado.")
                cluster.shutdown()
                print(f"Verificação de sincronização concluída para o nó {ip}.")
            except Exception as e:
                print(f"Erro ao conectar ao nó {ip}: {e}")


# Criar uma instância da classe SensorController
sensor_controller = SensorController()

# Manter o programa em execução indefinidamente
try:
    while True:
        pass
except KeyboardInterrupt:
    print("Programa interrompido pelo usuário.")

sensor_controller.cluster.shutdown()
