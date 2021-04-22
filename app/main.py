from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

@app.post("/getdata")
async def getdata():
    return { "error": "error getting tadaddddd"}

@app.post("/setdata")
async def setdata():
    return { "error": "error setting tadaddd"}
