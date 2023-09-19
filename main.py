from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse #, RedirectResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
# from replit import db #banco de dados da ReplIt
from pydantic import BaseModel #para auxiliar na documentação automática
from datetime import datetime
import uvicorn #para rodar o server


ORIGINS = ["*"]
METHODS = ["*"]
HEADERS = ["*"]

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            const hostProtocol = (window.location.host == '0.0.0.0:8080') ? 'ws' : 'wss'
            const ws = new WebSocket(`${hostProtocol}://${window.location.host}/ws`);
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""

# def fileToString(file_to_open):
#   content = ""
#   file = open(file_to_open, 'r')
#   for line in file:
#     content += line.replace("\n", "")
#   return content


# def getTime():
#   now = datetime.now()
#   current_time = now.strftime("%H:%M:%S")
#   return current_time


# class newIp(BaseModel):
  # external_IP: str


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
    return HTMLResponse(content=html,  status_code=200)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")


if __name__ == "__main__":
  print('Runing...')
  uvicorn.run(app, port=8080, host="0.0.0.0")
