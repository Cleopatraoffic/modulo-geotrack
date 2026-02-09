from fastapi import FastAPI, Request
import json
from datetime import datetime

app = FastAPI()

# Banco de dados temporário (em produção usaremos PostgreSQL)
DB_FILE = "coordinates.json"

@app.post("/track")
async def receive_data(request: Request):
    data = await request.json()
    data["server_time"] = datetime.now().isoformat()
    
    # Salva os dados recebidos (GPS + Wi-Fi + Bluetooth)
    with open(DB_FILE, "a") as f:
        f.write(json.dumps(data) + "\n")
    
    print(f"Dados recebidos de: {data.get('lat')}, {data.get('lon')}")
    return {"status": "success", "message": "Coordenadas capturadas"}

@app.get("/")
def home():
    return {"IA_Status": "Online", "Monitorando": True}