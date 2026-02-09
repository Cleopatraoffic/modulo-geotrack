from kivy.app import App
from kivy.uix.label import Label
from kivy.clock import Clock
from plyer import gps, wifi, bluetooth
from kivy.utils import platform
import json
import requests

# Só importa se estiver realmente rodando no celular
if platform == 'android':
    try:
        from android import android_service
    except ImportError:
        pass


class TrackerApp(App):
    def build(self):
        self.data_log = []
        self.label = Label(
            text="Rastreador IA: Ativo\nAguardando sinal...", halign="center")

        # Tenta iniciar o GPS (Update a cada 10 metros ou 30 segundos)
        try:
            gps.configure(on_location=self.on_location)
            gps.start(minTime=30000, minDistance=10)
        except NotImplementedError:
            self.label.text = "Erro: GPS não suportado no PC. Teste no Android."

        # Loop para capturar Wi-Fi e Bluetooth (o contexto da IA)
        Clock.schedule_interval(self.capture_context, 60)  # A cada 1 minuto
        return self.label

    def on_location(self, **kwargs):
        lat = kwargs.get('lat')
        lon = kwargs.get('lon')
        self.label.text = f"Localização Atual:\nLat: {lat}\nLon: {lon}"
        self.last_location = (lat, lon)

    def capture_context(self, dt):
        """Captura redes ao redor para a IA aprender o local"""
        context = {
            "coords": getattr(self, 'last_location', (0, 0)),
            "wifi_networks": self.get_wifi_scan(),
            "bt_devices": self.get_bluetooth_scan()
        }

        # Salva localmente caso o celular fique sem internet
        with open("tracker_data.json", "a") as f:
            f.write(json.dumps(context) + "\n")

        print("Snapshot capturado para IA.")

    def get_wifi_scan(self):
        try:
            return wifi.get_network_info()
        except:
            return []

    def get_bluetooth_scan(self):
        # Captura dispositivos Bluetooth próximos (Blotoff logic)
        try:
            return bluetooth.get_devices()
        except:
            return []

    def start_service(self):
    if platform == 'android':
        from android import android_service
        # O nome aqui deve ser o que definiremos no buildozer.spec
        android_service.start_service('geotrackpro', 'servico_ativo', '')

    def enviar_dados(payload):
    url = "https://seu-servidor.com/api/track" # Vamos criar isso já já
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers, timeout=5)
        return response.status_code == 200
    except:
        return False

if __name__ == "__main__":
    TrackerApp().run()
