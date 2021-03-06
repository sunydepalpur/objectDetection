import base64
import json
import logging

from flask import Flask
#from flask_sockets import Sockets
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

HTTP_SERVER_PORT = 5000

@socketio.on('/media')
def echo(ws):
    print("Connection accepted")
    # A lot of messages will be sent rapidly. We'll stop showing after the first one.
    has_seen_media = False
    message_count = 0
    while not ws.closed:
        message = ws.receive()
        if message is None:
            print("No message received...")
            continue

        # Messages are a JSON encoded string
        data = json.loads(message)

        # Using the event type you can determine what type of message you are receiving
        if data['event'] == "connected":
            print("Connected Message received: {}".format(message))
        if data['event'] == "start":
            print("Start Message received: {}".format(message))
        if data['event'] == "media":
            if not has_seen_media:
                print("Media message: {}".format(message))
                payload = data['media']['payload']
                print("Payload is: {}".format(payload))
                chunk = base64.b64decode(payload)
                print("That's {} bytes".format(len(chunk)))
                print("Additional media messages from WebSocket are being suppressed....")
                has_seen_media = True
        if data['event'] == "stop":
            print("Stop Message received: {}".format(message))
            break
        message_count += 1

    print("Connection closed. Received a total of {} messages".format(message_count))


if __name__ == '__main__':   
    socketio.run(app)
    print("Server listening on: http://localhost:" )