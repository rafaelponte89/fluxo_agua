# python3.6

import random
from datetime import datetime
from paho.mqtt import client as mqtt_client
import os

broker = 'broker.emqx.io'
port = 1883
topic = "emqx/fluxo_agua"
# Generate a Client ID with the subscribe prefix.
client_id = f'subscribe-{random.randint(0, 100)}'
#username = 'emqx'
#password = 'public'


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    #client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

#fluxo_total = 0.00

# salva o fluxo em um arquivo csv
def salvar_fluxo(msg_fluxo):
    #global fluxo_total
    #fluxo_total = fluxo_total + msg_fluxo + 0.12
    data = datetime.today()
    hora = data.strftime("%H:%M:%S")
    data = data.strftime("%d/%m/%Y")
    
    
    
    #print("Hora:",hora,"Minuto",minuto,"Segundo",segundo)
    if msg_fluxo > 0:
        try:
            with open("fluxoagua.csv","x") as file:
                file.writelines("medida,data,hora\n")
                file.writelines("{:.2f}, ".format(msg_fluxo))
                file.writelines(f"{data}, ")
                file.writelines(hora)
                file.writelines("\n")
        # sei que o arquivo mudou, pois
        except:
            with open("fluxoagua.csv","a") as file:
                file.writelines("{:.2f}, ".format(msg_fluxo))
                file.writelines(f"{data}, ")
                file.writelines(hora)
                file.writelines("\n")
        # sei que o arquivo mudou, pois o msg_fluxo > 0, sendo assim linhas serão escritas no arquivo
                
    
   
        #fluxo_total = 0
    #print("{:.2f}".format(fluxo_total))

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        salvar_fluxo(float(msg.payload.decode()))
        return f"{msg.payload.decode()}"

    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    
    client.loop_forever()


if __name__ == '__main__':
    run()
