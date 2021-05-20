from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import random

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8081",
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

emulators = {}

@app.post("/removeid")
async def removeId(reqId: ReqIdModel):
    print("removing id", reqId.id)
    if reqId.id in emulators.keys():
        del emulators[reqId.id]
        return {reqId.id}
    else:
        return {"error": "id not found"}

@app.post("/regid")
async def regId(regId: ReqIdModel):
    emulators[regId.id] =  DataModel()
    print("registrating new id: ", regId.id)
    return {"OK"}

@app.post("/getdata")
async def getdata(reqId: ReqIdModel):
    print("requesting data from id: ", reqId.id)
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
