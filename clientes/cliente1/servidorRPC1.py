import rpyc
from cassandra.cluster import Cluster
from cryptography.fernet import Fernet

#parâmetros banco de dados
cluster = Cluster(['172.20.0.2', '172.20.0.3'])
session = cluster.connect()
db_name = "dados" #Keyspace
table_name = "dados_idosos"

class servidorRPC(rpyc.Service):
    def __init__(self):
        super().__init__()
        # self.cipher_key = cipher_key

    def exposed_visualizar_dados(self):
        try:
            session.set_keyspace(db_name)

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

print("Iniciando o servidor")
server = ThreadedServer(servidorRPC, port=18861)
server.start()