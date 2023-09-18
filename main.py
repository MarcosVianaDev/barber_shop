from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from replit import db  #banco de dados da ReplIt
from pydantic import BaseModel
from datetime import datetime

# del db['previous_ips']
# db['previous_ips'] =

ORIGINS = ["*"]
METHODS = ["*"]
HEADERS = ["*"]


def read_HTML_Index():
  content = ""
  file = open("./index.html", 'r')
  for line in file:
    content += line.replace("\n", "")
  return content


def getTime():
  now = datetime.now()
  current_time = now.strftime("%H:%M:%S")
  return current_time


class newIp(BaseModel):
  external_IP: str


app = FastAPI()

app.add_middleware(
  CORSMiddleware,
  allow_origins=ORIGINS,
  allow_credentials=True,
  allow_methods=METHODS,
  allow_headers=HEADERS,
)


@app.get("/")
async def root():
  #print(read_HTML_Index())
  #return RedirectResponse("https://marcosvianadev.com.br/")
  return HTMLResponse(content=read_HTML_Index(), status_code=200)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
  await websocket.accept()
  while True:
    data = await websocket.receive_text()
    await websocket.send_text(f"Mensagem: {data}")


@app.get("/listkeys/")
async def listKeys():
  db_data = {}
  list_keys = db.keys()
  for key in list_keys:
    db_data[key] = db[key]
  return db_data


@app.get("/currentip/")
async def externalIp():
  return db["external_ip"]


@app.post("/setnewip/")
async def setExternalIp(ip: newIp):
  db["external_ip"] = ip.external_IP
  db['previous_ips'][getTime()] = ip.external_IP
  return {'status-code': 200}


@app.get("/dbshow/{key}")
async def subpage(key: str):
  return {key: db[f"{key}"]}


if __name__ == "__main__":
  print('Runing...')
  uvicorn.run(app, port=8080, host="0.0.0.0")
