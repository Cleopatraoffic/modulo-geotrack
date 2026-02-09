import time
from plyer import gps, wifi, bluetooth
from datetime import datetime
import requests

def enviar_para_nuvem(dados):
    # USE O IP QUE VOCÊ ANOTOU AQUI
    url = "http://136.115.253.109:8000/track"
    try:
        requests.post(url, json=dados, timeout=5)
    except:
        pass

class TrackerModule:
    def __init__(self):
        self.active = True
        
    def start_capture(self):
        # Inicia o sensor de GPS
        gps.configure(on_location=self.on_location_received)
        gps.start()
        
        while self.active:
            # Captura o "contexto" para a IA aprender
            context_data = {
                "time": datetime.now().isoformat(),
                "networks": self.scan_wifi(),
                "bt_devices": self.scan_bluetooth()
            }
            self.send_to_server(context_data)
            time.sleep(30) # Intervalo de 30 segundos

    def scan_wifi(self):
        # Pega SSIDs e intensidade de sinal (RSSI)
        # Isso alimenta a IA para saber 'onde' o celular está sem GPS
        try:
            return wifi.get_network_info()
        except:
            return []

    def on_location_received(self, **kwargs):
        print(f"Latitude: {kwargs['lat']}, Longitude: {kwargs['lon']}")

    def send_to_server(self, data):
        # Aqui conectaremos com a nossa API via POST ou MQTT
        print("Enviando dados para o servidor...")