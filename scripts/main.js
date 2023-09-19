const hostProtocol = (window.location.host == '0.0.0.0:8080') ? 'ws' : 'wss'

const ws = new WebSocket(`${hostProtocol}://${window.location.host}/ws`);

ws.onmessage = function(event) {
  let messages = document.getElementById('messages');
  let message = document.createElement('li');
  let content = document.createTextNode(event.data);
  message.appendChild(content)
  messages.appendChild(message)
}

function sendMessage(event) {
  const input = document.getElementById("messageText")
  ws.send(input.value)
  input.value = ''
  event.preventDefault()
}