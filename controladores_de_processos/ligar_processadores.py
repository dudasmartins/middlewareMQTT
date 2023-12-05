import subprocess
import time

def iniciar_controlador(numero):
    try:
        subprocess.Popen(['python3', f'controlador_processos_{numero}.py'])
        print(f"Controlador {numero} iniciado com sucesso.")
    except Exception as e:
        print(f"Erro ao iniciar o Controlador {numero}: {e}")


def desligar_controlador(numero):
    try:
        subprocess.run(['pkill', '-f', f'controlador_processos_{numero}.py'])
        print(f"Controlador {numero} encerrado com sucesso.")
    except Exception as e:
        print(f"Erro ao encerrar o Controlador {numero}: {e}")

def verificar_processo_em_execucao(numero):
    try:
        subprocess.run(['pgrep', '-f', f'controlador_processos_{numero}.py'], check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def alternar_controladores():
    mestre = 1
    escravo = 2
    controlador_ativo = mestre

    while True:
        # Iniciar o controlador ativo
        iniciar_controlador(controlador_ativo)
        print(f"Iniciando Controlador {controlador_ativo}.")

        # Aguardar até que o controlador ativo esteja em execução ou até que o intervalo de 1 segundo expire
        for _ in range(30):  # 30 iterações de 1 segundo = 30 segundos
            if verificar_processo_em_execucao(controlador_ativo):
                print(f"Controlador {controlador_ativo} está em execução. Aguardando 30 segundos para alternar.")
                for _ in range(30):  # 30 iterações de 1 segundo = 30 segundos
                    if not verificar_processo_em_execucao(controlador_ativo):
                        print(f"Controlador {controlador_ativo} foi encerrado. Alternando para o próximo controlador.")
                        break  # Sair do loop interno se o controlador foi encerrado
                    time.sleep(1)
                break  # Sair do loop externo se o controlador estiver em execução
            time.sleep(1)

        # Desligar o controlador ativo antes de alternar
        desligar_controlador(controlador_ativo)

        # Alternar para o próximo controlador
        controlador_ativo = escravo if controlador_ativo == mestre else mestre


if __name__ == "__main__":
    alternar_controladores()
