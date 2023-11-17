import paho.mqtt.client as paho
import time
import random
from datetime import datetime
from cryptography.fernet import Fernet

#Chave gerada manualmente
chave_criptografia = b'9i7e0z0FtQNjj85riGhBy7ZAdxTs8gPSg7BFIUrvka8='
cipher = Fernet(chave_criptografia)

broker="localhost"
port=1883
topic = "/nivel_oxigenio"

def on_publish(client, userdata, mid):
    print("Enviado")
    pass

client = paho.Client("admin")
client.on_publish = on_publish
client.connect(broker, port)

#while(True):
delay = random.randint(80, 90)
nivel_oxigenio = str(random.randint(0, 100))
data_atual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

data = nivel_oxigenio + ',' + data_atual

data_crypto = cipher.encrypt(data.encode()).decode()

client.publish(topic, data_crypto)
print(data)
#time.sleep(delay)
