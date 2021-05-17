from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://monitoremulator.com",
    "http://monitoremulator.com:8080",
    "http://www.monitoremulator.com",
    "http://www.monitoremulator.com:8080"
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
    hr: float
    sat_pre: float
    sat_post: float
    resp_rate: float
    etco2: float
    pfi: float
    temp: float
    abp_syst: float
    abp_diast: float


default_response_object = {
    'error': '',
    'id': '',
    'hr': 120,
    'sat_pre': 98,
    'sat_post': 95,
    'resp_rate': 30,
    'etco2': 4.5,
    'pfi': 1.5,
    'temp': 37.6,
    'abp_syst': 70,
    'abp_diast': 50
}

emulators = {}

@app.post("/removeid")
async def removeId(reqId: ReqIdModel):
    print("removing id", reqId.id)
    if reqId.id in emulators.keys():
        del emulators[reqId.id]
    return {'OK'}

@app.post("/reqid")
async def reqId(reqId: ReqIdModel):
    newObject = {
        'error': '',
        'id': reqId.id,
        'hr': 150,
        'sat_pre': 100,
        'sat_post': 100,
        'resp_rate': 35,
        'etco2': 5.0,
        'pfi': 1.1,
        'temp': 37.2,
        'abp_syst': 75,
        'abp_diast': 5
    }
    emulators[reqId.id] = newObject
    print("registrating new id: ", reqId.id)
    return {'OK'}

@app.post("/getdata")
async def getdata(reqId: ReqIdModel):
    print("requesting data from id: ", reqId.id)
    if reqId.id in emulators.keys():
        print(emulators[reqId.id])
        return emulators[reqId.id]
    else:
        print("requesting data not found for id: ", reqId.id)
        return {"error": "id not found"}

@app.post("/setdata")
async def setdata(newdata: DataModel):
    if newdata.id in emulators.keys():
        newObject = {
            'error': '',
            'id': newdata.id,
            'hr': newdata.hr,
            'sat_pre': newdata.sat_pre,
            'sat_post': newdata.sat_post,
            'resp_rate': newdata.resp_rate,
            'etco2': newdata.etco2,
            'pfi': newdata.pfi,
            'temp': newdata.temp,
            'abp_syst': newdata.abp_syst,
            'abp_diast': newdata.abp_diast
        }
        emulators[newdata.id] = newObject
        print("new data set for id: ", newObject['id'])
        return {"new data set"}
    else:
        print("error setting new data for id: ", newdata.id)
        return { "error": "id not found"}
