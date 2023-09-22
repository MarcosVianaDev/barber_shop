from typing import Annotated

from fastapi import (FastAPI, WebSocket, WebSocketException, HTTPException, status)
from fastapi.responses import HTMLResponse, JSONResponse

from fastapi.middleware.cors import CORSMiddleware

import barber_db_data as db

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
)


# @app.get("/")
# async def get():
#     return HTMLResponse(content=html, status_code=200)


@app.get("/{aba}/{id}")
async def getData(aba:str, id:str):
    resp = db.getData(aba=aba, id=id)
    if resp:
        return JSONResponse(resp)
    return JSONResponse(content = f'Id {id} not found' ,status_code=404)

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
