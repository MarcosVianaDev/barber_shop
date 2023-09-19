from typing import Annotated

from fastapi import (Cookie, Depends, FastAPI, Query, WebSocket,
                     WebSocketException, status)
from fastapi.responses import HTMLResponse  # , RedirectResponse, JSONResponse

# from fastapi.middleware.cors import CORSMiddleware
# from replit import db #banco de dados da ReplIt
import uvicorn  # para rodar o server

# ORIGINS = ["*"]
# METHODS = ["*"]
# HEADERS = ["*"]

html = """
<!DOCTYPE html>
<html>

<head>
<title>Chat com FastAPI</title>
</head>

<body>
<h1>Chat com FastAPI usando WebSocket</h1>
<form action="" onsubmit="sendMessage(event)">
<label>Item ID: <input type="text" id="itemId" autocomplete="off" value="foo"></label>
<label>Token: <input type="text" id="token" autocomplete="off" value="som-key-token"></label>
<button onclick="connect(event)">Conectar</button>
<hr>
<label>Mensagem: <input type="text" id="messageText" autocomplete="off" /></label>
<button>Enviar</button>
</form>
<ul id='messages'>
</ul>
<script>
const hostProtocol = (window.location.host == '0.0.0.0:8080' || window.location.host == 'localhost:8080') ? 'ws' : 'wss'
var ws = null;
function connect(event) {
var itemId = document.getElementById('itemId')
var token = document.getElementById('token')
ws = new WebSocket(`${hostProtocol}://${window.location.host}/items/${itemId.value}/ws?token=${token.value}`);

ws.onmessage = function (event) {
let messages = document.getElementById('messages');
let message = document.createElement('li');
let content = document.createTextNode(event.data);
message.appendChild(content)
messages.appendChild(message)
}
event.preventDefault()
}

function sendMessage(event) {
const input = document.getElementById("messageText")
ws.send(input.value)
input.value = ''
event.preventDefault()
}
</script>
</body>

</html>
"""

app = FastAPI()

# app.add_middleware(
#   CORSMiddleware,
#   allow_origins=ORIGINS,
#   allow_credentials=True,
#   allow_methods=METHODS,
#   allow_headers=HEADERS,
# )


@app.get("/")
async def get():
  return HTMLResponse(content=html, status_code=200)


async def get_cookie_or_token(websocket: WebSocket,
                              session: Annotated[str | None,
                                                 Cookie()] = None,
                              token: Annotated[str | None, Query()] = None):
  if session is None and token is None:
    raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
  return session or token


@app.websocket("/items/{item_id}/ws")
async def websocket_endpoint(
    *,
    websocket: WebSocket,
    item_id: str,
    q: int | None = None,
    cookie_or_token: Annotated[str, Depends(get_cookie_or_token)]):
  await websocket.accept()
  while True:
    data = await websocket.receive_text()
    await websocket.send_text(
        f"Valor da sessão ou do token é: {cookie_or_token}")
    if q is not None:
      await websocket.send_text(f'Valor do parametro Query "q" é: {q}')
    await websocket.send_text(
        f'Mensagem de texto: {data}, para o item: {item_id}')


if __name__ == "__main__":
  print('Runing...')
  uvicorn.run(app, port=8080, host="0.0.0.0")
