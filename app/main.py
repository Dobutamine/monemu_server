from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random, json


app = FastAPI()

origins = [
    "http://localhost",
    "ws://localhost",
    "http://localhost:8080",
    "http://localhost:8081",
    "ws://localhost:8080",
    "ws://localhost:8081",
    "http://monitoremulator.com",
    "http://monitoremulator.com:8080",
    "http://monitoremulator.com:8081",
    "http://www.monitoremulator.com",
    "http://www.monitoremulator.com:8080",
    "http://www.monitoremulator.com:8080",
    "http://104.248.90.19",
    "http://104.248.90.19:80",
    "http://104.248.90.19:8080",
    "http://104.248.90.19:8081",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ReqIdModel(BaseModel):
    id: str

class DataModel(BaseModel):
    id: str
    error: str
    heartrate: float
    satPre: float
    satPost: float
    satVen: float
    respRate: float
    etco2: float
    abpSyst: float
    abpDiast: float
    pfi: float
    temp: float
    cvp: float
    papSyst: float
    papDiast: float
    imageNo: float
    resusState: float
    rhythmType: float
    rhythmParameter: float
    curveSqueeze: float
    hrEnabled: bool
    satPreEnabled: bool
    satPostEnabled: bool
    satVenEnabled: bool
    abpEnabled: bool
    respRateEnabeld: bool
    etco2Enabled: bool
    tempEnabled: bool
    polsEnabled: bool
    pfiEnabled: bool
    nibdEnabled: bool
    cvpEnabled: bool
    papEnabled: bool
    alarmEnabled: bool

yoda_object = {
    'id': 'YODA',
    'error': '',
    'heartrate': 120,
    'satPre': 100,
    'satPost': 96,
    'satVen': 80,
    'respRate': 35,
    'etco2': 45,
    'abpSyst': 70,
    'abpDiast': 50,
    'pfi': 1.2,
    'temp': 37.1,
    'cvp': 4,
    'papSyst': 40,
    'papDiast': 20,
    'imageNo': 0,
    'resusState': 0,
    'rhythmType': 0,
    'rhythmParameter': 0,
    'curveSqueeze': 1,
    'hrEnabled': True,
    'satPreEnabled': True,
    'satPostEnabled': True,
    'satVenEnabled': False,
    'abpEnabled': True,
    'respRateEnabeld': True,
    'etco2Enabled': True,
    'tempEnabled': True,
    'polsEnabled': True,
    'pfiEnabled': True,
    'nibdEnabled': False,
    'cvpEnabled': False,
    'papEnabled': False,
    'alarmEnabled': True
}

empty_object = {
    'id': '',
    'error': '',
    'heartrate': 120,
    'satPre': 100,
    'satPost': 96,
    'satVen': 80,
    'respRate': 35,
    'etco2': 45,
    'abpSyst': 70,
    'abpDiast': 50,
    'pfi': 1.2,
    'temp': 37.1,
    'cvp': 4,
    'papSyst': 40,
    'papDiast': 20,
    'imageNo': 0,
    'resusState': 0,
    'rhythmType': 0,
    'rhythmParameter': 0,
    'curveSqueeze': 1,
    'hrEnabled': True,
    'satPreEnabled': True,
    'satPostEnabled': True,
    'satVenEnabled': False,
    'abpEnabled': True,
    'respRateEnabeld': True,
    'etco2Enabled': True,
    'tempEnabled': True,
    'polsEnabled': True,
    'pfiEnabled': True,
    'nibdEnabled': False,
    'cvpEnabled': False,
    'papEnabled': False,
    'alarmEnabled': True
}

emulators = {
    'YODA': yoda_object
}

registered_users = ['YODA']

@app.websocket("/ws_get")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            # wait for any message from the client in json form and converted it to a dictionary
            received_message =  await websocket.receive_json()

            if (received_message['command'] == 'close'):
                await websocket.send_json("OK")
                break

            if (received_message['command'] == 'remove'):
                if received_message['id'] in registered_users:
                    del emulators[received_message['id']]
                    await websocket.send_json("OK")
                else:
                    await websocket.send_json("id not found")
                continue
            
            if (received_message['command'] == 'register'):
                if (received_message['id'] not in registered_users):
                    registered_users.append(received_message['id'])
                    await websocket.send_json("OK")
                continue
            
            if (received_message['command'] == 'set'):
                if received_message['id'] in registered_users:
                    emulators[received_message['id']] = received_message
                    await websocket.send_json("OK")
                continue

            if (received_message['command'] == 'get'):
                if received_message['id'] in registered_users:
                    await websocket.send_json(emulators[received_message['id']])
                continue

        except Exception as e:
            print('error: ', e)
            break
