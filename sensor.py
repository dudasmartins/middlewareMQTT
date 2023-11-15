import paho.mqtt.client as mqtt
import time
import random
from datetime import datetime
from cryptography.fernet import Fernet

# Chave gerada manualmente
chave_criptografia = b'9i7e0z0FtQNjj85riGhBy7ZAdxTs8gPSg7BFIUrvka8='
cipher = Fernet(chave_criptografia)

# Configurações do Broker MQTT
broker_address = "localhost"  # Endereço do broker MQTT
port = 1883  # Porta padrão do MQTT
topic = "/saude"

client = mqtt.Client("Gerador_Dados")
client.connect(broker_address, port)

def on_publish(client, userdata, mid):
    print("enviado")
    pass

client.on_publish = on_publish

while True:
    saturacao = str(random.randint(90,100))
    insulina = str(random.uniform(70,150))
    pressao_sistolica = str(random.randint(90,120))
    pressao_diastolica = str(random.randint(60,80))
    data_atual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    dados_saude = f"{saturacao},{insulina},{pressao_sistolica},{pressao_diastolica},{data_atual}"

    # Criptografar os dados
    dados_crypto = cipher.encrypt(dados_saude.encode()).decode()

    client.publish(topic, dados_crypto)

    print(dados_saude)

    time.sleep(30)