from datetime import date
from typing import Annotated

from fastapi import (FastAPI, Body, WebSocket, WebSocketException, status)
from fastapi.responses import JSONResponse, HTMLResponse

from fastapi.middleware.cors import CORSMiddleware

from tiny_db import Barber_DB

db = Barber_DB()

ORIGINS = ["*"]
METHODS = ["*"]
HEADERS = ["*"]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=METHODS,
    allow_headers=HEADERS,
    # exposed_headers= HEADERS,
)


@app.get('/')
def handleRoot():
  return HTMLResponse(content="<h1>Barber Shop API</h1>", status_code=status.HTTP_200_OK)

@app.post("/{aba}/new")
async def postData(aba: str, data: Annotated[dict, Body()]):
  result = {'aba não encontrada'}
  data[
      'data_cadastro'] = f'{date.today().day}/{date.today().month}/{date.today().year}'
  if (aba == 'barbeiros'):
    result = db.create_Barbeiro(data)
  elif (aba == 'barbearias'):
    result = db.create_Barbearia(data)
  elif (aba == 'proprietarios'):
    result = db.create_Proprietario(data)
  return JSONResponse(content=result, status_code=status.HTTP_201_CREATED)


@app.put("/{aba}/{id}/edit")
async def updateData(aba: str, id: int, data: Annotated[dict, Body()]):
  if (aba == 'barbeiro'):
    result = db.set_Barbeiro(id, data)
  elif (aba == 'barbearia'):
    result = db.set_Barbearia(id, data)
  elif (aba == 'proprietario'):
    result = db.set_Proprietario(id, data)
  return JSONResponse(content=result, status_code=status.HTTP_202_ACCEPTED)


@app.get("/{aba}/{id}")
async def getData(aba: str, id: int):
  result = None
  if (aba == 'barbeiro'):
    result = db.get_Barbeiro(id)
  elif (aba == 'barbearia'):
    result = db.get_Barbearia(id)
  elif (aba == 'proprietario'):
    result = db.get_Proprietario(id)
  if result:
    return JSONResponse(result, headers={"Referrer-Policy": "unsafe-url"})
  return JSONResponse(content=f'Id {id} not found',
                      status_code=status.HTTP_404_NOT_FOUND)


#
# @app.websocket("/items/{item_id}/ws")
# async def websocket_endpoint(*,
#                              websocket: WebSocket,
#                              item_id: str,
#                              q: int | None = None,
#                              token: Annotated[str | None, Query()] = None):
#     await websocket.accept()
#     while True:
#         data = await websocket.receive_text()
#         await websocket.send_text(
#             f"Valor do token é: {token}")
#         if q is not None:
#             await websocket.send_text(f'Valor do parametro Query "q" é: {q}')
#         await websocket.send_text(
#             f'Mensagem de texto: {data}, para o item: {item_id}')

if __name__ == "__main__":
  import uvicorn  # para rodar o server
  print('Runing...')
  uvicorn.run(app, port=7733, host="0.0.0.0")
