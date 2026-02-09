# service.py
from time import sleep
from plyer import gps

def start_tracking():
    while True:
        # Aqui vai a lógica de capturar e enviar para o servidor
        print("Serviço de rastreio a correr em background...")
        sleep(60) # Espera 1 minuto para não gastar muita bateria

if __name__ == '__main__':
    start_tracking()