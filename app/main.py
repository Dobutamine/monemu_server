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

print("testing1")

emulators = {
    'YODA': yoda_object
}

@app.websocket("/ws_set")
async def websocket_endpoint(websocket: WebSocket):
    print('Accepting client connection...')
    await websocket.accept()
    while True:
        try:
            # wait for any message from the client in json form and converted it to a dictionary
            received_message =  json.loads(await websocket.receive_json())
            # send message to the client
            message = { 'value': random.uniform(0, 1) }
            await websocket.send_json(message)
        except Exception as e:
            print('error: ', e)
            break
    print('Bye')

@app.websocket("/ws_get")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            # wait for any message from the client in json form and converted it to a dictionary
            received_message =  await websocket.receive_json()

            if (received_message['command'] == 'close'):
                await websocket.send_json("closing")

            if received_message['id'] in emulators.keys():
                await websocket.send_json(emulators[received_message['id']])




            # received_message = json.loads(received_message)

            # # check what the command is 
            # if (received_message['command'] == 'close'):
            #     break

            # if received_message['id'] in emulators.keys():
            #     await websocket.send_json(emulators[received_message['id']])

            
        except Exception as e:
            print('error: ', e)
            break
    print('Bye')


@app.post("/removeid")
async def removeId(reqId: ReqIdModel):
    if reqId.id in emulators.keys():
        del emulators[reqId.id]
        return {"OK"}
    else:
        return {"error": "id not found"}

@app.post("/regid")
async def regId(regId: ReqIdModel):
    emulators[regId.id] =  DataModel()
    print("registrating new id: ", regId.id)
    return {"OK"}

@app.post("/getdata")
async def getdata(reqId: ReqIdModel):
    if reqId.id in emulators.keys():
        return emulators[reqId.id]
    else:
        print("requesting data not found for id: ", reqId.id)
        return {"error": "id not found"}

@app.post("/setdata")
async def setdata(newdata: DataModel):
    if newdata.id in emulators.keys():
        emulators[newdata.id] = newdata
        return {"OK"}
    else:
        print("error setting new data for id: ", newdata.id)
        return { "error": "id not found"}
