import rpyc
from cassandra.cluster import Cluster
from cryptography.fernet import Fernet

#parâmetros de conexão banco de dados
cluster = Cluster(['172.19.0.2'])  # endereço servidor cassandra
session = cluster.connect('data')  # "keyspace" banco de dados


class servidorRPC(rpyc.Service):
    def __init__(self, cipher_key):
        super().__init__()
        self.cipher_key = cipher_key

    # # Salvar dados criptografados no Cassandra
    # def exposed_salvar_dados_criptografados(self, dado_criptografado):
    #     try:
    #         cipher = Fernet(self.cipher_key)
    #         dado_descriptografado = cipher.decrypt(dado_criptografado.encode()).decode()
    #         salvar_dados_cassandra(*map(float, dado_descriptografado.split(',')))
    #         return True
    #     except Exception as e:
    #         print(f"Erro ao salvar dados no Cassandra: {e}")
    #         return False

    # Função para salvar dados no Cassandra

    def exposed_retorna_todos_os_dados():
        select_query = "SELECT * FROM old_people;"

chave_criptografia = b'9i7e0z0FtQNjj85riGhBy7ZAdxTs8gPSg7BFIUrvka8='

if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer

server = ThreadedServer(servidorRPC(chave_criptografia), port=18862)
server.start()