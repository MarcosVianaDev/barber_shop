from typing import Annotated

from fastapi import (FastAPI, Body, WebSocket, WebSocketException, status)
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from fastapi.middleware.cors import CORSMiddleware

import barber_db_data as db

ORIGINS = ["*"]
METHODS = ["*"]
HEADERS = ["*"]


# class barbeiro(BaseModel):
#     nome: str
#     apelido: str
#     data_cadastro: str
#     local_trabalho: str
#     ativo: str


# class barbearia(BaseModel):
#     nome: str
#     data_cadastro: str
#     responsavel: str
#     email: str
#     telefone: str
#     cep: str
#     ativo: str


# class proprietario(BaseModel):
#     nome: str
#     data_cadastro: str
#     dono_de: str
#     telefone: str
#     email: str
#     ativo: str


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=METHODS,
    allow_headers=HEADERS,
    # exposed_headers= HEADERS,
)


@app.post("/{aba}/new")
async def postData(aba: str, data: Annotated[dict, Body()]):
    result = {'aba não encontrada'}
    if (aba == 'barbeiros'):
        result = db.createData(aba=aba, nome=data['nome'], apelido=data['apelido'], local_trabalho=data['local_trabalho'], ativo='1')
    elif (aba == 'barbearias'):
        result = db.createData(aba=aba, nome=data['nome'], responsavel=data['responsavel'], email=data['email'], telefone=data['telefone'], cep=data['cep'], ativo=data['ativo'])
    elif (aba == 'proprietarios'):
        result = db.createData(aba=aba, nome=data['nome'], dono_de=data['dono_de'], telefone=data['telefone'], email=data['email'], ativo=data['ativo'])
    return JSONResponse(content=result, status_code=status.HTTP_201_CREATED)


@app.put("/{aba}/{id}/edit")
async def updateData(aba: str, id: str, data: Annotated[dict, Body()]):
    print(data)
    if (aba == 'barbeiros'):
        result = db.updateData(aba=aba, id=id, nome=data['nome'], data_cadastro=data['data_cadastro'], ativo=data['ativo'], apelido=data['apelido'], local_trabalho=data['local_trabalho'])
    elif (aba == 'barbearias'):
        result = db.updateData(aba=aba, id=id, nome=data['nome'], responsavel=data['responsavel'], data_cadastro=data['data_cadastro'], ativo=data['ativo'], cep=data['cep'], email=data['email'], telefone=data['telefone'])
    elif (aba == 'proprietarios'):
        result = db.updateData(aba=aba, id=id, nome=data['nome'], dono_de=data['dono_de'], data_cadastro=data['data_cadastro'], ativo=data['ativo'],  email=data['email'], telefone=data['telefone'])
    return JSONResponse(content=result, status_code=status.HTTP_202_ACCEPTED)


@app.get("/{aba}/{id}")
async def getData(aba: str, id: str):
    resp = db.getData(aba=aba, id=id)
    if resp:
        return JSONResponse(resp, headers={"Referrer-Policy":"unsafe-url"})
    return JSONResponse(content=f'Id {id} not found', status_code=status.HTTP_404_NOT_FOUND)
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
    uvicorn.run(app, port=8080, host="0.0.0.0")
