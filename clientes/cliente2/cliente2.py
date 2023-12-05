import rpyc
import json
from cassandra.cluster import Cluster

porta_control1 = 18861

def visualizar_dados():
    try:
        # Conexão com o servidor RPC
        proxy_control = rpyc.connect('localhost', porta_control1, config={'allow_public_attrs': True, 'sync_request_timeout': 1})
    except ConnectionRefusedError as e:
        print("Erro: Servidor RPC indisponível")
        return

    try:
        # Obtém dados do servidor RPC chamando o método remoto 'visualizar_dados'
        dados = proxy_control.root.visualizar_dados()

        # Converte os dados obtidos em um formato JSON específico
        json_data = json.dumps([{'nivel_oxigenio': item['nivel_oxigenio'], 'data_hora': item['data_atual']} for item in dados])

        # Imprime os dados
        print("Dados:")
        for item in dados:
            print(f"Nível de Oxigênio: {item['nivel_oxigenio']}, Data e Hora: {item['data_atual']}")

    except Exception as e:
        print(f"Erro ao visualizar dados: {e}")
    finally:
        proxy_control.close()

if __name__ == "__main__":
    while True:
        print("Escolha uma opção:")
        print("1. Visualizar dados")
        print("2. Sair")

        escolha = input("Digite o número da opção: ")

        if escolha == "1":
            visualizar_dados()
        elif escolha == "2":
            print("Saindo do programa.")
            break
        else:
            print("Opção inválida. Tente novamente.")
