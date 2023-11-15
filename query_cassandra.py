from cassandra.cluster import Cluster

# Conecta ao cluster
cluster = Cluster(['172.19.0.2'])  # Substitua 'localhost' pelo endereço do seu servidor Cassandra
session = cluster.connect('data')  # Substitua 'data' pelo nome do seu keyspace

# Executa uma consulta
query = "SELECT * FROM old_people;"
rows = session.execute(query)

# Exibe os resultados
for row in rows:
    print(row)

# Fecha a conexão
cluster.shutdown()
