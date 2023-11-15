import paho.mqtt.client as mqtt

broker="localhost"
port=1883

# email_enviar = "mariaeduarda_martins97@hotmail.com"
# email_senha = "teste"
# email_receiver =  "dudasmartins97@gmail.com"

def on_connect(client, userdata, flags, rc):
    client.subscribe("/enviar_notificacao_idoso")

def on_menssage(client, userdata, msg):

    global dados_atuais

    dados = msg.payload.decode()

    saturacao = dados.split(',')[0]
    insulina = dados.split(',')[1]
    pressao_sistolica = dados.split(',')[2]
    pressao_diastolica = dados.split(',')[3]
    data_atual = dados.split(',')[4]

    print('ENIANDO ALERTA DE RISCO')
    print(f'SAUTRAÇÃO: {saturacao} | Insulina: {insulina} | Pressão sistólica: {pressao_sistolica} | Pressão diastólica: {pressao_diastolica} | Data: {data_atual}')



# definir atuação
client = mqtt.Client()
client.connect(broker, port)
client.on_connect = on_connect
client.on_message = on_message
client.loop_forever()
