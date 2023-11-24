import rpyc
import json

porta_control1 = 18861
porta_control2 = 18862

def visualizar_dados():
    try:
        # Conexão com o servidor RPC
        proxy_control = rpyc.connect('localhost', porta_control1, config={'allow_public_attrs': True, 'sync_request_timeout': 60})
    except ConnectionRefusedError as e:
        print("Erro: Servidor RPC 1 indisponível", e)

        try:
            #tenta conexão no controlador 2
            proxy_control = rpyc.connect('localhost', porta_control2, config={'allow_public_attrs': True, 'sync_request_timeout': 60})
        except ConnectionRefusedError as e:
            print("Erro: Servidor RPC 2 indisponível", e)
            print("Erro: Nenhum dos servidores disponíveis.")

    try:
        # Obtém dados do servidor RPC chamando o método remoto 'visualizar_dados'
        dados = proxy_control.root.visualizar_dados()
        for item in dados:
            print(f"Nível de Oxigênio: {item['nivel_oxigenio']}, \tData e Hora: {item['data_atual']}")

    except Exception as e:
        print(f"Erro ao visualizar dados: {e}")


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
