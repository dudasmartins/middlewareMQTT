import rpyc
from cassandra.cluster import Cluster
from cryptography.fernet import Fernet

#parâmetros banco de dados
cluster = Cluster(['cassandra-node1', 'cassandra-node2'])
session = cluster.connect()
db_name = "dados" #Keyspace
table_name = "dados_idosos"

class servidorRPC(rpyc.Service):
    def __init__(self, cipher_key):
        super().__init__()
        self.cipher_key = cipher_key

    def exposed_visualizar_dados():
        try:
            # Conectar ao cluster Cassandra com fallback para o segundo nó em caso de falha
            cluster = Cluster(['cassandra-node1', 'cassandra-node2'])
            session = cluster.connect('dados')

            # Query para selecionar todos os dados da tabela
            query = f"SELECT * FROM {table_name}"
            rows = session.execute(query)

            # Converter os resultados em uma lista de dicionários
            dados = [{'id': str(row.id), 'nivel_oxigenio': row.nivel_oxigenio, 'data_atual': row.data_atual} for row in rows]

            return dados

        except Exception as e:
            return f'Erro ao visualizar dados: {e}'

        finally:
            cluster.shutdown()




if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer

server = ThreadedServer(servidorRPC(chave_criptografia), port=18862)
server.start()