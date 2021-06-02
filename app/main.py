from fastapi import FastAPI, WebSocket
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "ws://localhost",
    "ws://localhost",
    "ws://localhost:8080",
    "ws://localhost:8081",
    "ws://localhost:8080",
    "ws://localhost:8081",
    "ws://monitoremulator.com",
    "ws://monitoremulator.com:8080",
    "ws://monitoremulator.com:8081",
    "ws://www.monitoremulator.com",
    "ws://www.monitoremulator.com:8080",
    "ws://www.monitoremulator.com:8080",
    "ws://104.248.90.19",
    "ws://104.248.90.19:80",
    "ws://104.248.90.19:8080",
    "ws://104.248.90.19:8081",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

emulators = {
    'YODA': {},
    'LEIA': {}
}

registered_users = ['YODA', 'HAN', 'LEIA', 'LUKE', 'OBI-WAN', 'KYLO', 'R2-D2', 'C-3PO']

@app.get("/library")
def image():
    return FileResponse("library/pneumothorax_right.png")



@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            # wait for any message from the client in json form and converted it to a dictionary
            received_message =  await websocket.receive_json()

            if (received_message['command'] == 'close'):
                await websocket.send_json("connection closed")
                break

            if (received_message['command'] == 'remove'):
                if received_message['id'] in registered_users:
                    del emulators[received_message['id']]
                    await websocket.send_json("OK")
                else:
                    await websocket.send_json("id not registered")
                continue
            
            if (received_message['command'] == 'register'):
                if (received_message['id'] not in registered_users):
                    registered_users.append(received_message['id'])
                    await websocket.send_json("OK")
                else:
                    await websocket.send_json("id already registered")
                continue
            
            if (received_message['command'] == 'set'):
                if received_message['id'] in registered_users:
                    emulators[received_message['id']] = received_message
                    await websocket.send_json("data updated")
                else:
                    await websocket.send_json("id not registered")
                continue

            if (received_message['command'] == 'get'):
                if received_message['id'] in registered_users:
                    if received_message['id'] in emulators:
                        await websocket.send_json(emulators[received_message['id']])
                    else:
                        await websocket.send_json('bo data')
                else:
                    await websocket.send_json('id not registered')
                continue
                

        except Exception as e:
            print('error: ', e)
            break
