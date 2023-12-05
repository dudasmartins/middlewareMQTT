import paho.mqtt.client as mqtt

broker="localhost"
port=1883

def on_connect(client, userdata, flags, rc):
    client.subscribe("/notificacao")

def on_message(client, userdata, msg):
    global dados_atuais

    #decodificar a mensagem recebida
    dados = msg.payload.decode()

    #oxigenio vai na pposição 0 e a data na posição 1
    nivel_oxigenio = dados.split(',')[0]
    data_atual = dados.split(',')[1]

    print('#########################################')
    print('Gerando notificação para o responsável!')
    print(f'Nível de oxigênio: {nivel_oxigenio} | Data: {data_atual}')

# configuração MQTT
client = mqtt.Client()
client.connect(broker, port)
client.on_connect = on_connect
client.on_message = on_message
client.loop_forever()